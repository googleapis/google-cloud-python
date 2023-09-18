# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from typing import Dict, Mapping, MutableMapping, MutableSequence, Optional, Sequence, Tuple, Type, Union

from google.iam_v1beta import gapic_version as package_version

from google.api_core.client_options import ClientOptions
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials   # type: ignore
from google.oauth2 import service_account              # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.iam_v1beta.services.workload_identity_pools import pagers
from google.iam_v1beta.types import workload_identity_pool
from google.iam_v1beta.types import workload_identity_pool as gi_workload_identity_pool
from google.protobuf import field_mask_pb2  # type: ignore
from .transports.base import WorkloadIdentityPoolsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import WorkloadIdentityPoolsGrpcAsyncIOTransport
from .client import WorkloadIdentityPoolsClient


class WorkloadIdentityPoolsAsyncClient:
    """Manages WorkloadIdentityPools."""

    _client: WorkloadIdentityPoolsClient

    DEFAULT_ENDPOINT = WorkloadIdentityPoolsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = WorkloadIdentityPoolsClient.DEFAULT_MTLS_ENDPOINT

    workload_identity_pool_path = staticmethod(WorkloadIdentityPoolsClient.workload_identity_pool_path)
    parse_workload_identity_pool_path = staticmethod(WorkloadIdentityPoolsClient.parse_workload_identity_pool_path)
    workload_identity_pool_provider_path = staticmethod(WorkloadIdentityPoolsClient.workload_identity_pool_provider_path)
    parse_workload_identity_pool_provider_path = staticmethod(WorkloadIdentityPoolsClient.parse_workload_identity_pool_provider_path)
    common_billing_account_path = staticmethod(WorkloadIdentityPoolsClient.common_billing_account_path)
    parse_common_billing_account_path = staticmethod(WorkloadIdentityPoolsClient.parse_common_billing_account_path)
    common_folder_path = staticmethod(WorkloadIdentityPoolsClient.common_folder_path)
    parse_common_folder_path = staticmethod(WorkloadIdentityPoolsClient.parse_common_folder_path)
    common_organization_path = staticmethod(WorkloadIdentityPoolsClient.common_organization_path)
    parse_common_organization_path = staticmethod(WorkloadIdentityPoolsClient.parse_common_organization_path)
    common_project_path = staticmethod(WorkloadIdentityPoolsClient.common_project_path)
    parse_common_project_path = staticmethod(WorkloadIdentityPoolsClient.parse_common_project_path)
    common_location_path = staticmethod(WorkloadIdentityPoolsClient.common_location_path)
    parse_common_location_path = staticmethod(WorkloadIdentityPoolsClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            WorkloadIdentityPoolsAsyncClient: The constructed client.
        """
        return WorkloadIdentityPoolsClient.from_service_account_info.__func__(WorkloadIdentityPoolsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            WorkloadIdentityPoolsAsyncClient: The constructed client.
        """
        return WorkloadIdentityPoolsClient.from_service_account_file.__func__(WorkloadIdentityPoolsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @classmethod
    def get_mtls_endpoint_and_cert_source(cls, client_options: Optional[ClientOptions] = None):
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
        return WorkloadIdentityPoolsClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> WorkloadIdentityPoolsTransport:
        """Returns the transport used by the client instance.

        Returns:
            WorkloadIdentityPoolsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(type(WorkloadIdentityPoolsClient).get_transport_class, type(WorkloadIdentityPoolsClient))

    def __init__(self, *,
            credentials: Optional[ga_credentials.Credentials] = None,
            transport: Union[str, WorkloadIdentityPoolsTransport] = "grpc_asyncio",
            client_options: Optional[ClientOptions] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            ) -> None:
        """Instantiates the workload identity pools client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.WorkloadIdentityPoolsTransport]): The
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
        self._client = WorkloadIdentityPoolsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,

        )

    async def list_workload_identity_pools(self,
            request: Optional[Union[workload_identity_pool.ListWorkloadIdentityPoolsRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListWorkloadIdentityPoolsAsyncPager:
        r"""Lists all non-deleted
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool]s
        in a project. If ``show_deleted`` is set to ``true``, then
        deleted pools are also listed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_list_workload_identity_pools():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                request = iam_v1beta.ListWorkloadIdentityPoolsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_workload_identity_pools(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.ListWorkloadIdentityPoolsRequest, dict]]):
                The request object. Request message for
                ListWorkloadIdentityPools.
            parent (:class:`str`):
                Required. The parent resource to list
                pools for.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam_v1beta.services.workload_identity_pools.pagers.ListWorkloadIdentityPoolsAsyncPager:
                Response message for
                ListWorkloadIdentityPools.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = workload_identity_pool.ListWorkloadIdentityPoolsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_workload_identity_pools,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
        response = pagers.ListWorkloadIdentityPoolsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_workload_identity_pool(self,
            request: Optional[Union[workload_identity_pool.GetWorkloadIdentityPoolRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> workload_identity_pool.WorkloadIdentityPool:
        r"""Gets an individual
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_get_workload_identity_pool():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                request = iam_v1beta.GetWorkloadIdentityPoolRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_workload_identity_pool(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.GetWorkloadIdentityPoolRequest, dict]]):
                The request object. Request message for
                GetWorkloadIdentityPool.
            name (:class:`str`):
                Required. The name of the pool to
                retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam_v1beta.types.WorkloadIdentityPool:
                Represents a collection of external
                workload identities. You can define IAM
                policies to grant these identities
                access to Google Cloud resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = workload_identity_pool.GetWorkloadIdentityPoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_workload_identity_pool,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    async def create_workload_identity_pool(self,
            request: Optional[Union[gi_workload_identity_pool.CreateWorkloadIdentityPoolRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            workload_identity_pool: Optional[gi_workload_identity_pool.WorkloadIdentityPool] = None,
            workload_identity_pool_id: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Creates a new
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        You cannot reuse the name of a deleted pool until 30 days after
        deletion.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_create_workload_identity_pool():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                request = iam_v1beta.CreateWorkloadIdentityPoolRequest(
                    parent="parent_value",
                    workload_identity_pool_id="workload_identity_pool_id_value",
                )

                # Make the request
                operation = client.create_workload_identity_pool(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.CreateWorkloadIdentityPoolRequest, dict]]):
                The request object. Request message for
                CreateWorkloadIdentityPool.
            parent (:class:`str`):
                Required. The parent resource to create the pool in. The
                only supported location is ``global``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workload_identity_pool (:class:`google.iam_v1beta.types.WorkloadIdentityPool`):
                Required. The pool to create.
                This corresponds to the ``workload_identity_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workload_identity_pool_id (:class:`str`):
                Required. The ID to use for the pool, which becomes the
                final component of the resource name. This value should
                be 4-32 characters, and may contain the characters
                [a-z0-9-]. The prefix ``gcp-`` is reserved for use by
                Google, and may not be specified.

                This corresponds to the ``workload_identity_pool_id`` field
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

                The result type for the operation will be :class:`google.iam_v1beta.types.WorkloadIdentityPool` Represents a collection of external workload identities. You can define IAM
                   policies to grant these identities access to Google
                   Cloud resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, workload_identity_pool, workload_identity_pool_id])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = gi_workload_identity_pool.CreateWorkloadIdentityPoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if workload_identity_pool is not None:
            request.workload_identity_pool = workload_identity_pool
        if workload_identity_pool_id is not None:
            request.workload_identity_pool_id = workload_identity_pool_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_workload_identity_pool,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
            gi_workload_identity_pool.WorkloadIdentityPool,
            metadata_type=gi_workload_identity_pool.WorkloadIdentityPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_workload_identity_pool(self,
            request: Optional[Union[gi_workload_identity_pool.UpdateWorkloadIdentityPoolRequest, dict]] = None,
            *,
            workload_identity_pool: Optional[gi_workload_identity_pool.WorkloadIdentityPool] = None,
            update_mask: Optional[field_mask_pb2.FieldMask] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Updates an existing
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_update_workload_identity_pool():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                request = iam_v1beta.UpdateWorkloadIdentityPoolRequest(
                )

                # Make the request
                operation = client.update_workload_identity_pool(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.UpdateWorkloadIdentityPoolRequest, dict]]):
                The request object. Request message for
                UpdateWorkloadIdentityPool.
            workload_identity_pool (:class:`google.iam_v1beta.types.WorkloadIdentityPool`):
                Required. The pool to update. The ``name`` field is used
                to identify the pool.

                This corresponds to the ``workload_identity_pool`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields update.
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

                The result type for the operation will be :class:`google.iam_v1beta.types.WorkloadIdentityPool` Represents a collection of external workload identities. You can define IAM
                   policies to grant these identities access to Google
                   Cloud resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([workload_identity_pool, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = gi_workload_identity_pool.UpdateWorkloadIdentityPoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if workload_identity_pool is not None:
            request.workload_identity_pool = workload_identity_pool
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_workload_identity_pool,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("workload_identity_pool.name", request.workload_identity_pool.name),
            )),
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
            gi_workload_identity_pool.WorkloadIdentityPool,
            metadata_type=gi_workload_identity_pool.WorkloadIdentityPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_workload_identity_pool(self,
            request: Optional[Union[workload_identity_pool.DeleteWorkloadIdentityPoolRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Deletes a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        You cannot use a deleted pool to exchange external credentials
        for Google Cloud credentials. However, deletion does not revoke
        credentials that have already been issued. Credentials issued
        for a deleted pool do not grant access to resources. If the pool
        is undeleted, and the credentials are not expired, they grant
        access again. You can undelete a pool for 30 days. After 30
        days, deletion is permanent. You cannot update deleted pools.
        However, you can view and list them.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_delete_workload_identity_pool():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                request = iam_v1beta.DeleteWorkloadIdentityPoolRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_workload_identity_pool(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.DeleteWorkloadIdentityPoolRequest, dict]]):
                The request object. Request message for
                DeleteWorkloadIdentityPool.
            name (:class:`str`):
                Required. The name of the pool to
                delete.

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

                The result type for the operation will be :class:`google.iam_v1beta.types.WorkloadIdentityPool` Represents a collection of external workload identities. You can define IAM
                   policies to grant these identities access to Google
                   Cloud resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = workload_identity_pool.DeleteWorkloadIdentityPoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_workload_identity_pool,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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
            workload_identity_pool.WorkloadIdentityPool,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    async def undelete_workload_identity_pool(self,
            request: Optional[Union[workload_identity_pool.UndeleteWorkloadIdentityPoolRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Undeletes a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool],
        as long as it was deleted fewer than 30 days ago.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_undelete_workload_identity_pool():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                request = iam_v1beta.UndeleteWorkloadIdentityPoolRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.undelete_workload_identity_pool(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.UndeleteWorkloadIdentityPoolRequest, dict]]):
                The request object. Request message for
                UndeleteWorkloadIdentityPool.
            name (:class:`str`):
                Required. The name of the pool to
                undelete.

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

                The result type for the operation will be :class:`google.iam_v1beta.types.WorkloadIdentityPool` Represents a collection of external workload identities. You can define IAM
                   policies to grant these identities access to Google
                   Cloud resources.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = workload_identity_pool.UndeleteWorkloadIdentityPoolRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.undelete_workload_identity_pool,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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
            workload_identity_pool.WorkloadIdentityPool,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolOperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_workload_identity_pool_providers(self,
            request: Optional[Union[workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> pagers.ListWorkloadIdentityPoolProvidersAsyncPager:
        r"""Lists all non-deleted
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityPoolProvider]s
        in a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].
        If ``show_deleted`` is set to ``true``, then deleted providers
        are also listed.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_list_workload_identity_pool_providers():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                request = iam_v1beta.ListWorkloadIdentityPoolProvidersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_workload_identity_pool_providers(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.ListWorkloadIdentityPoolProvidersRequest, dict]]):
                The request object. Request message for
                ListWorkloadIdentityPoolProviders.
            parent (:class:`str`):
                Required. The pool to list providers
                for.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam_v1beta.services.workload_identity_pools.pagers.ListWorkloadIdentityPoolProvidersAsyncPager:
                Response message for
                ListWorkloadIdentityPoolProviders.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = workload_identity_pool.ListWorkloadIdentityPoolProvidersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_workload_identity_pool_providers,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
        response = pagers.ListWorkloadIdentityPoolProvidersAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_workload_identity_pool_provider(self,
            request: Optional[Union[workload_identity_pool.GetWorkloadIdentityPoolProviderRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> workload_identity_pool.WorkloadIdentityPoolProvider:
        r"""Gets an individual
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityPoolProvider].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_get_workload_identity_pool_provider():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                request = iam_v1beta.GetWorkloadIdentityPoolProviderRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_workload_identity_pool_provider(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.GetWorkloadIdentityPoolProviderRequest, dict]]):
                The request object. Request message for
                GetWorkloadIdentityPoolProvider.
            name (:class:`str`):
                Required. The name of the provider to
                retrieve.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam_v1beta.types.WorkloadIdentityPoolProvider:
                A configuration for an external
                identity provider.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = workload_identity_pool.GetWorkloadIdentityPoolProviderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_workload_identity_pool_provider,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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

    async def create_workload_identity_pool_provider(self,
            request: Optional[Union[workload_identity_pool.CreateWorkloadIdentityPoolProviderRequest, dict]] = None,
            *,
            parent: Optional[str] = None,
            workload_identity_pool_provider: Optional[workload_identity_pool.WorkloadIdentityPoolProvider] = None,
            workload_identity_pool_provider_id: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Creates a new
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider]
        in a
        [WorkloadIdentityPool][google.iam.v1beta.WorkloadIdentityPool].

        You cannot reuse the name of a deleted provider until 30 days
        after deletion.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_create_workload_identity_pool_provider():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                workload_identity_pool_provider = iam_v1beta.WorkloadIdentityPoolProvider()
                workload_identity_pool_provider.aws.account_id = "account_id_value"

                request = iam_v1beta.CreateWorkloadIdentityPoolProviderRequest(
                    parent="parent_value",
                    workload_identity_pool_provider=workload_identity_pool_provider,
                    workload_identity_pool_provider_id="workload_identity_pool_provider_id_value",
                )

                # Make the request
                operation = client.create_workload_identity_pool_provider(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.CreateWorkloadIdentityPoolProviderRequest, dict]]):
                The request object. Request message for
                CreateWorkloadIdentityPoolProvider.
            parent (:class:`str`):
                Required. The pool to create this
                provider in.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workload_identity_pool_provider (:class:`google.iam_v1beta.types.WorkloadIdentityPoolProvider`):
                Required. The provider to create.
                This corresponds to the ``workload_identity_pool_provider`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workload_identity_pool_provider_id (:class:`str`):
                Required. The ID for the provider, which becomes the
                final component of the resource name. This value must be
                4-32 characters, and may contain the characters
                [a-z0-9-]. The prefix ``gcp-`` is reserved for use by
                Google, and may not be specified.

                This corresponds to the ``workload_identity_pool_provider_id`` field
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
                :class:`google.iam_v1beta.types.WorkloadIdentityPoolProvider`
                A configuration for an external identity provider.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, workload_identity_pool_provider, workload_identity_pool_provider_id])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = workload_identity_pool.CreateWorkloadIdentityPoolProviderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if workload_identity_pool_provider is not None:
            request.workload_identity_pool_provider = workload_identity_pool_provider
        if workload_identity_pool_provider_id is not None:
            request.workload_identity_pool_provider_id = workload_identity_pool_provider_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_workload_identity_pool_provider,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("parent", request.parent),
            )),
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
            workload_identity_pool.WorkloadIdentityPoolProvider,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolProviderOperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_workload_identity_pool_provider(self,
            request: Optional[Union[workload_identity_pool.UpdateWorkloadIdentityPoolProviderRequest, dict]] = None,
            *,
            workload_identity_pool_provider: Optional[workload_identity_pool.WorkloadIdentityPoolProvider] = None,
            update_mask: Optional[field_mask_pb2.FieldMask] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Updates an existing
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_update_workload_identity_pool_provider():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                workload_identity_pool_provider = iam_v1beta.WorkloadIdentityPoolProvider()
                workload_identity_pool_provider.aws.account_id = "account_id_value"

                request = iam_v1beta.UpdateWorkloadIdentityPoolProviderRequest(
                    workload_identity_pool_provider=workload_identity_pool_provider,
                )

                # Make the request
                operation = client.update_workload_identity_pool_provider(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.UpdateWorkloadIdentityPoolProviderRequest, dict]]):
                The request object. Request message for
                UpdateWorkloadIdentityPoolProvider.
            workload_identity_pool_provider (:class:`google.iam_v1beta.types.WorkloadIdentityPoolProvider`):
                Required. The provider to update.
                This corresponds to the ``workload_identity_pool_provider`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The list of fields to
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
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.iam_v1beta.types.WorkloadIdentityPoolProvider`
                A configuration for an external identity provider.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([workload_identity_pool_provider, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = workload_identity_pool.UpdateWorkloadIdentityPoolProviderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if workload_identity_pool_provider is not None:
            request.workload_identity_pool_provider = workload_identity_pool_provider
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_workload_identity_pool_provider,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("workload_identity_pool_provider.name", request.workload_identity_pool_provider.name),
            )),
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
            workload_identity_pool.WorkloadIdentityPoolProvider,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolProviderOperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_workload_identity_pool_provider(self,
            request: Optional[Union[workload_identity_pool.DeleteWorkloadIdentityPoolProviderRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Deletes a
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider].
        Deleting a provider does not revoke credentials that have
        already been issued; they continue to grant access. You can
        undelete a provider for 30 days. After 30 days, deletion is
        permanent. You cannot update deleted providers. However, you can
        view and list them.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_delete_workload_identity_pool_provider():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                request = iam_v1beta.DeleteWorkloadIdentityPoolProviderRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_workload_identity_pool_provider(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.DeleteWorkloadIdentityPoolProviderRequest, dict]]):
                The request object. Request message for
                DeleteWorkloadIdentityPoolProvider.
            name (:class:`str`):
                Required. The name of the provider to
                delete.

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
                :class:`google.iam_v1beta.types.WorkloadIdentityPoolProvider`
                A configuration for an external identity provider.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = workload_identity_pool.DeleteWorkloadIdentityPoolProviderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_workload_identity_pool_provider,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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
            workload_identity_pool.WorkloadIdentityPoolProvider,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolProviderOperationMetadata,
        )

        # Done; return the response.
        return response

    async def undelete_workload_identity_pool_provider(self,
            request: Optional[Union[workload_identity_pool.UndeleteWorkloadIdentityPoolProviderRequest, dict]] = None,
            *,
            name: Optional[str] = None,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Union[float, object] = gapic_v1.method.DEFAULT,
            metadata: Sequence[Tuple[str, str]] = (),
            ) -> operation_async.AsyncOperation:
        r"""Undeletes a
        [WorkloadIdentityPoolProvider][google.iam.v1beta.WorkloadIdentityProvider],
        as long as it was deleted fewer than 30 days ago.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google import iam_v1beta

            async def sample_undelete_workload_identity_pool_provider():
                # Create a client
                client = iam_v1beta.WorkloadIdentityPoolsAsyncClient()

                # Initialize request argument(s)
                request = iam_v1beta.UndeleteWorkloadIdentityPoolProviderRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.undelete_workload_identity_pool_provider(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.iam_v1beta.types.UndeleteWorkloadIdentityPoolProviderRequest, dict]]):
                The request object. Request message for
                UndeleteWorkloadIdentityPoolProvider.
            name (:class:`str`):
                Required. The name of the provider to
                undelete.

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
                :class:`google.iam_v1beta.types.WorkloadIdentityPoolProvider`
                A configuration for an external identity provider.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError("If the `request` argument is set, then none of "
                             "the individual field arguments should be set.")

        request = workload_identity_pool.UndeleteWorkloadIdentityPoolProviderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.undelete_workload_identity_pool_provider,
            default_retry=retries.Retry(
initial=1.0,maximum=10.0,multiplier=1.3,                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata((
                ("name", request.name),
            )),
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
            workload_identity_pool.WorkloadIdentityPoolProvider,
            metadata_type=workload_identity_pool.WorkloadIdentityPoolProviderOperationMetadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "WorkloadIdentityPoolsAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(gapic_version=package_version.__version__)


__all__ = (
    "WorkloadIdentityPoolsAsyncClient",
)
