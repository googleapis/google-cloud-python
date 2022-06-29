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
from typing import Dict, Mapping, Optional, Sequence, Tuple, Type, Union
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
from .transports.grpc_asyncio import BackupForGKEGrpcAsyncIOTransport
from .client import BackupForGKEClient


class BackupForGKEAsyncClient:
    """BackupForGKE allows Kubernetes administrators to configure,
    execute, and manage backup and restore operations for their GKE
    clusters.
    """

    _client: BackupForGKEClient

    DEFAULT_ENDPOINT = BackupForGKEClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = BackupForGKEClient.DEFAULT_MTLS_ENDPOINT

    backup_path = staticmethod(BackupForGKEClient.backup_path)
    parse_backup_path = staticmethod(BackupForGKEClient.parse_backup_path)
    backup_plan_path = staticmethod(BackupForGKEClient.backup_plan_path)
    parse_backup_plan_path = staticmethod(BackupForGKEClient.parse_backup_plan_path)
    cluster_path = staticmethod(BackupForGKEClient.cluster_path)
    parse_cluster_path = staticmethod(BackupForGKEClient.parse_cluster_path)
    crypto_key_path = staticmethod(BackupForGKEClient.crypto_key_path)
    parse_crypto_key_path = staticmethod(BackupForGKEClient.parse_crypto_key_path)
    restore_path = staticmethod(BackupForGKEClient.restore_path)
    parse_restore_path = staticmethod(BackupForGKEClient.parse_restore_path)
    restore_plan_path = staticmethod(BackupForGKEClient.restore_plan_path)
    parse_restore_plan_path = staticmethod(BackupForGKEClient.parse_restore_plan_path)
    volume_backup_path = staticmethod(BackupForGKEClient.volume_backup_path)
    parse_volume_backup_path = staticmethod(BackupForGKEClient.parse_volume_backup_path)
    volume_restore_path = staticmethod(BackupForGKEClient.volume_restore_path)
    parse_volume_restore_path = staticmethod(
        BackupForGKEClient.parse_volume_restore_path
    )
    common_billing_account_path = staticmethod(
        BackupForGKEClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        BackupForGKEClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(BackupForGKEClient.common_folder_path)
    parse_common_folder_path = staticmethod(BackupForGKEClient.parse_common_folder_path)
    common_organization_path = staticmethod(BackupForGKEClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        BackupForGKEClient.parse_common_organization_path
    )
    common_project_path = staticmethod(BackupForGKEClient.common_project_path)
    parse_common_project_path = staticmethod(
        BackupForGKEClient.parse_common_project_path
    )
    common_location_path = staticmethod(BackupForGKEClient.common_location_path)
    parse_common_location_path = staticmethod(
        BackupForGKEClient.parse_common_location_path
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
            BackupForGKEAsyncClient: The constructed client.
        """
        return BackupForGKEClient.from_service_account_info.__func__(BackupForGKEAsyncClient, info, *args, **kwargs)  # type: ignore

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
            BackupForGKEAsyncClient: The constructed client.
        """
        return BackupForGKEClient.from_service_account_file.__func__(BackupForGKEAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return BackupForGKEClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> BackupForGKETransport:
        """Returns the transport used by the client instance.

        Returns:
            BackupForGKETransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(BackupForGKEClient).get_transport_class, type(BackupForGKEClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, BackupForGKETransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the backup for gke client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.BackupForGKETransport]): The
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
        self._client = BackupForGKEClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_backup_plan(
        self,
        request: Union[gkebackup.CreateBackupPlanRequest, dict] = None,
        *,
        parent: str = None,
        backup_plan: gcg_backup_plan.BackupPlan = None,
        backup_plan_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new BackupPlan in a given location.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_create_backup_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

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

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.CreateBackupPlanRequest, dict]):
                The request object. Request message for
                CreateBackupPlan.
            parent (:class:`str`):
                Required. The location within which to create the
                BackupPlan. Format: ``projects/*/locations/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_plan (:class:`google.cloud.gke_backup_v1.types.BackupPlan`):
                Required. The BackupPlan resource
                object to create.

                This corresponds to the ``backup_plan`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_plan_id (:class:`str`):
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
            google.api_core.operation_async.AsyncOperation:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_backup_plan,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcg_backup_plan.BackupPlan,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_backup_plans(
        self,
        request: Union[gkebackup.ListBackupPlansRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBackupPlansAsyncPager:
        r"""Lists BackupPlans in a given location.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_list_backup_plans():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListBackupPlansRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_backup_plans(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListBackupPlansRequest, dict]):
                The request object. Request message for ListBackupPlans.
            parent (:class:`str`):
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
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListBackupPlansAsyncPager:
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

        request = gkebackup.ListBackupPlansRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_backup_plans,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = pagers.ListBackupPlansAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_backup_plan(
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

            async def sample_get_backup_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetBackupPlanRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_backup_plan(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetBackupPlanRequest, dict]):
                The request object. Request message for GetBackupPlan.
            name (:class:`str`):
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

        request = gkebackup.GetBackupPlanRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_backup_plan,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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

    async def update_backup_plan(
        self,
        request: Union[gkebackup.UpdateBackupPlanRequest, dict] = None,
        *,
        backup_plan: gcg_backup_plan.BackupPlan = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Update a BackupPlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_update_backup_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                backup_plan = gke_backup_v1.BackupPlan()
                backup_plan.cluster = "cluster_value"

                request = gke_backup_v1.UpdateBackupPlanRequest(
                    backup_plan=backup_plan,
                )

                # Make the request
                operation = client.update_backup_plan(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.UpdateBackupPlanRequest, dict]):
                The request object. Request message for
                UpdateBackupPlan.
            backup_plan (:class:`google.cloud.gke_backup_v1.types.BackupPlan`):
                Required. A new version of the BackupPlan resource that
                contains updated fields. This may be sparsely populated
                if an ``update_mask`` is provided.

                This corresponds to the ``backup_plan`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
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
            google.api_core.operation_async.AsyncOperation:
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

        request = gkebackup.UpdateBackupPlanRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if backup_plan is not None:
            request.backup_plan = backup_plan
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_backup_plan,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("backup_plan.name", request.backup_plan.name),)
            ),
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
            gcg_backup_plan.BackupPlan,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_backup_plan(
        self,
        request: Union[gkebackup.DeleteBackupPlanRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes an existing BackupPlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_delete_backup_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.DeleteBackupPlanRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_backup_plan(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.DeleteBackupPlanRequest, dict]):
                The request object. Request message for
                DeleteBackupPlan.
            name (:class:`str`):
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

        request = gkebackup.DeleteBackupPlanRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_backup_plan,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def create_backup(
        self,
        request: Union[gkebackup.CreateBackupRequest, dict] = None,
        *,
        parent: str = None,
        backup: gcg_backup.Backup = None,
        backup_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a Backup for the given BackupPlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_create_backup():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.CreateBackupRequest(
                    parent="parent_value",
                )

                # Make the request
                operation = client.create_backup(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.CreateBackupRequest, dict]):
                The request object. Request message for CreateBackup.
            parent (:class:`str`):
                Required. The BackupPlan within which to create the
                Backup. Format: ``projects/*/locations/*/backupPlans/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup (:class:`google.cloud.gke_backup_v1.types.Backup`):
                The Backup resource to create.
                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_id (:class:`str`):
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
            google.api_core.operation_async.AsyncOperation:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_backup,
            default_timeout=120.0,
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
            gcg_backup.Backup,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_backups(
        self,
        request: Union[gkebackup.ListBackupsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBackupsAsyncPager:
        r"""Lists the Backups for a given BackupPlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_list_backups():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListBackupsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_backups(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListBackupsRequest, dict]):
                The request object. Request message for ListBackups.
            parent (:class:`str`):
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
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListBackupsAsyncPager:
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

        request = gkebackup.ListBackupsRequest(request)

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
                multiplier=1.3,
                predicate=retries.if_exception_type(
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

    async def get_backup(
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

            async def sample_get_backup():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetBackupRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_backup(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetBackupRequest, dict]):
                The request object. Request message for GetBackup.
            name (:class:`str`):
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

        request = gkebackup.GetBackupRequest(request)

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
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        request: Union[gkebackup.UpdateBackupRequest, dict] = None,
        *,
        backup: gcg_backup.Backup = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Update a Backup.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_update_backup():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                backup = gke_backup_v1.Backup()
                backup.all_namespaces = True

                request = gke_backup_v1.UpdateBackupRequest(
                    backup=backup,
                )

                # Make the request
                operation = client.update_backup(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.UpdateBackupRequest, dict]):
                The request object. Request message for UpdateBackup.
            backup (:class:`google.cloud.gke_backup_v1.types.Backup`):
                Required. A new version of the Backup resource that
                contains updated fields. This may be sparsely populated
                if an ``update_mask`` is provided.

                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
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
            google.api_core.operation_async.AsyncOperation:
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

        request = gkebackup.UpdateBackupRequest(request)

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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcg_backup.Backup,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_backup(
        self,
        request: Union[gkebackup.DeleteBackupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes an existing Backup.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_delete_backup():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.DeleteBackupRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_backup(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.DeleteBackupRequest, dict]):
                The request object. Request message for DeleteBackup.
            name (:class:`str`):
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

        request = gkebackup.DeleteBackupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_backup,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_volume_backups(
        self,
        request: Union[gkebackup.ListVolumeBackupsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVolumeBackupsAsyncPager:
        r"""Lists the VolumeBackups for a given Backup.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_list_volume_backups():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListVolumeBackupsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_volume_backups(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListVolumeBackupsRequest, dict]):
                The request object. Request message for
                ListVolumeBackups.
            parent (:class:`str`):
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
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListVolumeBackupsAsyncPager:
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

        request = gkebackup.ListVolumeBackupsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_volume_backups,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = pagers.ListVolumeBackupsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_volume_backup(
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

            async def sample_get_volume_backup():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetVolumeBackupRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_volume_backup(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetVolumeBackupRequest, dict]):
                The request object. Request message for GetVolumeBackup.
            name (:class:`str`):
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

        request = gkebackup.GetVolumeBackupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_volume_backup,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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

    async def create_restore_plan(
        self,
        request: Union[gkebackup.CreateRestorePlanRequest, dict] = None,
        *,
        parent: str = None,
        restore_plan: gcg_restore_plan.RestorePlan = None,
        restore_plan_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new RestorePlan in a given location.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_create_restore_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

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

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.CreateRestorePlanRequest, dict]):
                The request object. Request message for
                CreateRestorePlan.
            parent (:class:`str`):
                Required. The location within which to create the
                RestorePlan. Format: ``projects/*/locations/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            restore_plan (:class:`google.cloud.gke_backup_v1.types.RestorePlan`):
                Required. The RestorePlan resource
                object to create.

                This corresponds to the ``restore_plan`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            restore_plan_id (:class:`str`):
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
            google.api_core.operation_async.AsyncOperation:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_restore_plan,
            default_timeout=120.0,
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
            gcg_restore_plan.RestorePlan,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_restore_plans(
        self,
        request: Union[gkebackup.ListRestorePlansRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRestorePlansAsyncPager:
        r"""Lists RestorePlans in a given location.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_list_restore_plans():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListRestorePlansRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_restore_plans(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListRestorePlansRequest, dict]):
                The request object. Request message for
                ListRestorePlans.
            parent (:class:`str`):
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
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListRestorePlansAsyncPager:
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

        request = gkebackup.ListRestorePlansRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_restore_plans,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = pagers.ListRestorePlansAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_restore_plan(
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

            async def sample_get_restore_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetRestorePlanRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_restore_plan(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetRestorePlanRequest, dict]):
                The request object. Request message for GetRestorePlan.
            name (:class:`str`):
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

        request = gkebackup.GetRestorePlanRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_restore_plan,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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

    async def update_restore_plan(
        self,
        request: Union[gkebackup.UpdateRestorePlanRequest, dict] = None,
        *,
        restore_plan: gcg_restore_plan.RestorePlan = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Update a RestorePlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_update_restore_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

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

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.UpdateRestorePlanRequest, dict]):
                The request object. Request message for
                UpdateRestorePlan.
            restore_plan (:class:`google.cloud.gke_backup_v1.types.RestorePlan`):
                Required. A new version of the RestorePlan resource that
                contains updated fields. This may be sparsely populated
                if an ``update_mask`` is provided.

                This corresponds to the ``restore_plan`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
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
            google.api_core.operation_async.AsyncOperation:
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

        request = gkebackup.UpdateRestorePlanRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if restore_plan is not None:
            request.restore_plan = restore_plan
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_restore_plan,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("restore_plan.name", request.restore_plan.name),)
            ),
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
            gcg_restore_plan.RestorePlan,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_restore_plan(
        self,
        request: Union[gkebackup.DeleteRestorePlanRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes an existing RestorePlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_delete_restore_plan():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.DeleteRestorePlanRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_restore_plan(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.DeleteRestorePlanRequest, dict]):
                The request object. Request message for
                DeleteRestorePlan.
            name (:class:`str`):
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

        request = gkebackup.DeleteRestorePlanRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_restore_plan,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def create_restore(
        self,
        request: Union[gkebackup.CreateRestoreRequest, dict] = None,
        *,
        parent: str = None,
        restore: gcg_restore.Restore = None,
        restore_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Restore for the given RestorePlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_create_restore():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

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

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.CreateRestoreRequest, dict]):
                The request object. Request message for CreateRestore.
            parent (:class:`str`):
                Required. The RestorePlan within which to create the
                Restore. Format:
                ``projects/*/locations/*/restorePlans/*``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            restore (:class:`google.cloud.gke_backup_v1.types.Restore`):
                Required. The restore resource to
                create.

                This corresponds to the ``restore`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            restore_id (:class:`str`):
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
            google.api_core.operation_async.AsyncOperation:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_restore,
            default_timeout=120.0,
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
            gcg_restore.Restore,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_restores(
        self,
        request: Union[gkebackup.ListRestoresRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRestoresAsyncPager:
        r"""Lists the Restores for a given RestorePlan.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_list_restores():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListRestoresRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_restores(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListRestoresRequest, dict]):
                The request object. Request message for ListRestores.
            parent (:class:`str`):
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
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListRestoresAsyncPager:
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

        request = gkebackup.ListRestoresRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_restores,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = pagers.ListRestoresAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_restore(
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

            async def sample_get_restore():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetRestoreRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_restore(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetRestoreRequest, dict]):
                The request object. Request message for GetRestore.
            name (:class:`str`):
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

        request = gkebackup.GetRestoreRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_restore,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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

    async def update_restore(
        self,
        request: Union[gkebackup.UpdateRestoreRequest, dict] = None,
        *,
        restore: gcg_restore.Restore = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Update a Restore.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_update_restore():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                restore = gke_backup_v1.Restore()
                restore.backup = "backup_value"

                request = gke_backup_v1.UpdateRestoreRequest(
                    restore=restore,
                )

                # Make the request
                operation = client.update_restore(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.UpdateRestoreRequest, dict]):
                The request object. Request message for UpdateRestore.
            restore (:class:`google.cloud.gke_backup_v1.types.Restore`):
                Required. A new version of the Restore resource that
                contains updated fields. This may be sparsely populated
                if an ``update_mask`` is provided.

                This corresponds to the ``restore`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
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
            google.api_core.operation_async.AsyncOperation:
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

        request = gkebackup.UpdateRestoreRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if restore is not None:
            request.restore = restore
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_restore,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("restore.name", request.restore.name),)
            ),
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
            gcg_restore.Restore,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_restore(
        self,
        request: Union[gkebackup.DeleteRestoreRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes an existing Restore.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_delete_restore():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.DeleteRestoreRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_restore(request=request)

                print("Waiting for operation to complete...")

                response = await operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.DeleteRestoreRequest, dict]):
                The request object. Request message for DeleteRestore.
            name (:class:`str`):
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

        request = gkebackup.DeleteRestoreRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_restore,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=gkebackup.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_volume_restores(
        self,
        request: Union[gkebackup.ListVolumeRestoresRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListVolumeRestoresAsyncPager:
        r"""Lists the VolumeRestores for a given Restore.

        .. code-block:: python

            from google.cloud import gke_backup_v1

            async def sample_list_volume_restores():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.ListVolumeRestoresRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_volume_restores(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.ListVolumeRestoresRequest, dict]):
                The request object. Request message for
                ListVolumeRestores.
            parent (:class:`str`):
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
            google.cloud.gke_backup_v1.services.backup_for_gke.pagers.ListVolumeRestoresAsyncPager:
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

        request = gkebackup.ListVolumeRestoresRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_volume_restores,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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
        response = pagers.ListVolumeRestoresAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_volume_restore(
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

            async def sample_get_volume_restore():
                # Create a client
                client = gke_backup_v1.BackupForGKEAsyncClient()

                # Initialize request argument(s)
                request = gke_backup_v1.GetVolumeRestoreRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_volume_restore(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.gke_backup_v1.types.GetVolumeRestoreRequest, dict]):
                The request object. Request message for
                GetVolumeRestore.
            name (:class:`str`):
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

        request = gkebackup.GetVolumeRestoreRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_volume_restore,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-gke-backup",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BackupForGKEAsyncClient",)
