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

from google.cloud.dataform_v1alpha2.services.dataform import pagers
from google.cloud.dataform_v1alpha2.types import dataform
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.type import interval_pb2  # type: ignore
from .transports.base import DataformTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import DataformGrpcAsyncIOTransport
from .client import DataformClient


class DataformAsyncClient:
    """Dataform is a service to develop, create, document, test, and
    update curated tables in BigQuery.
    """

    _client: DataformClient

    DEFAULT_ENDPOINT = DataformClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DataformClient.DEFAULT_MTLS_ENDPOINT

    compilation_result_path = staticmethod(DataformClient.compilation_result_path)
    parse_compilation_result_path = staticmethod(
        DataformClient.parse_compilation_result_path
    )
    repository_path = staticmethod(DataformClient.repository_path)
    parse_repository_path = staticmethod(DataformClient.parse_repository_path)
    secret_version_path = staticmethod(DataformClient.secret_version_path)
    parse_secret_version_path = staticmethod(DataformClient.parse_secret_version_path)
    workflow_invocation_path = staticmethod(DataformClient.workflow_invocation_path)
    parse_workflow_invocation_path = staticmethod(
        DataformClient.parse_workflow_invocation_path
    )
    workspace_path = staticmethod(DataformClient.workspace_path)
    parse_workspace_path = staticmethod(DataformClient.parse_workspace_path)
    common_billing_account_path = staticmethod(
        DataformClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        DataformClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(DataformClient.common_folder_path)
    parse_common_folder_path = staticmethod(DataformClient.parse_common_folder_path)
    common_organization_path = staticmethod(DataformClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        DataformClient.parse_common_organization_path
    )
    common_project_path = staticmethod(DataformClient.common_project_path)
    parse_common_project_path = staticmethod(DataformClient.parse_common_project_path)
    common_location_path = staticmethod(DataformClient.common_location_path)
    parse_common_location_path = staticmethod(DataformClient.parse_common_location_path)

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DataformAsyncClient: The constructed client.
        """
        return DataformClient.from_service_account_info.__func__(DataformAsyncClient, info, *args, **kwargs)  # type: ignore

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
            DataformAsyncClient: The constructed client.
        """
        return DataformClient.from_service_account_file.__func__(DataformAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return DataformClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> DataformTransport:
        """Returns the transport used by the client instance.

        Returns:
            DataformTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(DataformClient).get_transport_class, type(DataformClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, DataformTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the dataform client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.DataformTransport]): The
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
        self._client = DataformClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_repositories(
        self,
        request: Union[dataform.ListRepositoriesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRepositoriesAsyncPager:
        r"""Lists Repositories in a given project and location.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_list_repositories():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.ListRepositoriesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_repositories(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.ListRepositoriesRequest, dict]):
                The request object. `ListRepositories` request message.
            parent (:class:`str`):
                Required. The location in which to list repositories.
                Must be in the format ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.services.dataform.pagers.ListRepositoriesAsyncPager:
                ListRepositories response message.

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

        request = dataform.ListRepositoriesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_repositories,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListRepositoriesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_repository(
        self,
        request: Union[dataform.GetRepositoryRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.Repository:
        r"""Fetches a single Repository.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_get_repository():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.GetRepositoryRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_repository(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.GetRepositoryRequest, dict]):
                The request object. `GetRepository` request message.
            name (:class:`str`):
                Required. The repository's name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.Repository:
                Represents a Dataform Git repository.
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

        request = dataform.GetRepositoryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_repository,
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

        # Done; return the response.
        return response

    async def create_repository(
        self,
        request: Union[dataform.CreateRepositoryRequest, dict] = None,
        *,
        parent: str = None,
        repository: dataform.Repository = None,
        repository_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.Repository:
        r"""Creates a new Repository in a given project and
        location.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_create_repository():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.CreateRepositoryRequest(
                    parent="parent_value",
                    repository_id="repository_id_value",
                )

                # Make the request
                response = await client.create_repository(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.CreateRepositoryRequest, dict]):
                The request object. `CreateRepository` request message.
            parent (:class:`str`):
                Required. The location in which to create the
                repository. Must be in the format
                ``projects/*/locations/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            repository (:class:`google.cloud.dataform_v1alpha2.types.Repository`):
                Required. The repository to create.
                This corresponds to the ``repository`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            repository_id (:class:`str`):
                Required. The ID to use for the
                repository, which will become the final
                component of the repository's resource
                name.

                This corresponds to the ``repository_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.Repository:
                Represents a Dataform Git repository.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, repository, repository_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = dataform.CreateRepositoryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if repository is not None:
            request.repository = repository
        if repository_id is not None:
            request.repository_id = repository_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_repository,
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

        # Done; return the response.
        return response

    async def update_repository(
        self,
        request: Union[dataform.UpdateRepositoryRequest, dict] = None,
        *,
        repository: dataform.Repository = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.Repository:
        r"""Updates a single Repository.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_update_repository():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.UpdateRepositoryRequest(
                )

                # Make the request
                response = await client.update_repository(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.UpdateRepositoryRequest, dict]):
                The request object. `UpdateRepository` request message.
            repository (:class:`google.cloud.dataform_v1alpha2.types.Repository`):
                Required. The repository to update.
                This corresponds to the ``repository`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Optional. Specifies the fields to be
                updated in the repository. If left
                unset, all fields will be updated.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.Repository:
                Represents a Dataform Git repository.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([repository, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = dataform.UpdateRepositoryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if repository is not None:
            request.repository = repository
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_repository,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("repository.name", request.repository.name),)
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

    async def delete_repository(
        self,
        request: Union[dataform.DeleteRepositoryRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a single Repository.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_delete_repository():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.DeleteRepositoryRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_repository(request=request)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.DeleteRepositoryRequest, dict]):
                The request object. `DeleteRepository` request message.
            name (:class:`str`):
                Required. The repository's name.
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

        request = dataform.DeleteRepositoryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_repository,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def fetch_remote_branches(
        self,
        request: Union[dataform.FetchRemoteBranchesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.FetchRemoteBranchesResponse:
        r"""Fetches a Repository's remote branches.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_fetch_remote_branches():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.FetchRemoteBranchesRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.fetch_remote_branches(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.FetchRemoteBranchesRequest, dict]):
                The request object. `FetchRemoteBranches` request
                message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.FetchRemoteBranchesResponse:
                FetchRemoteBranches response message.
        """
        # Create or coerce a protobuf request object.
        request = dataform.FetchRemoteBranchesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.fetch_remote_branches,
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

        # Done; return the response.
        return response

    async def list_workspaces(
        self,
        request: Union[dataform.ListWorkspacesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListWorkspacesAsyncPager:
        r"""Lists Workspaces in a given Repository.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_list_workspaces():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.ListWorkspacesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_workspaces(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.ListWorkspacesRequest, dict]):
                The request object. `ListWorkspaces` request message.
            parent (:class:`str`):
                Required. The repository in which to list workspaces.
                Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.services.dataform.pagers.ListWorkspacesAsyncPager:
                ListWorkspaces response message.

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

        request = dataform.ListWorkspacesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_workspaces,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListWorkspacesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_workspace(
        self,
        request: Union[dataform.GetWorkspaceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.Workspace:
        r"""Fetches a single Workspace.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_get_workspace():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.GetWorkspaceRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_workspace(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.GetWorkspaceRequest, dict]):
                The request object. `GetWorkspace` request message.
            name (:class:`str`):
                Required. The workspace's name.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.Workspace:
                Represents a Dataform Git workspace.
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

        request = dataform.GetWorkspaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_workspace,
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

        # Done; return the response.
        return response

    async def create_workspace(
        self,
        request: Union[dataform.CreateWorkspaceRequest, dict] = None,
        *,
        parent: str = None,
        workspace: dataform.Workspace = None,
        workspace_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.Workspace:
        r"""Creates a new Workspace in a given Repository.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_create_workspace():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.CreateWorkspaceRequest(
                    parent="parent_value",
                    workspace_id="workspace_id_value",
                )

                # Make the request
                response = await client.create_workspace(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.CreateWorkspaceRequest, dict]):
                The request object. `CreateWorkspace` request message.
            parent (:class:`str`):
                Required. The repository in which to create the
                workspace. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workspace (:class:`google.cloud.dataform_v1alpha2.types.Workspace`):
                Required. The workspace to create.
                This corresponds to the ``workspace`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workspace_id (:class:`str`):
                Required. The ID to use for the
                workspace, which will become the final
                component of the workspace's resource
                name.

                This corresponds to the ``workspace_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.Workspace:
                Represents a Dataform Git workspace.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, workspace, workspace_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = dataform.CreateWorkspaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if workspace is not None:
            request.workspace = workspace
        if workspace_id is not None:
            request.workspace_id = workspace_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_workspace,
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

        # Done; return the response.
        return response

    async def delete_workspace(
        self,
        request: Union[dataform.DeleteWorkspaceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a single Workspace.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_delete_workspace():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.DeleteWorkspaceRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_workspace(request=request)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.DeleteWorkspaceRequest, dict]):
                The request object. `DeleteWorkspace` request message.
            name (:class:`str`):
                Required. The workspace resource's
                name.

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

        request = dataform.DeleteWorkspaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_workspace,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def install_npm_packages(
        self,
        request: Union[dataform.InstallNpmPackagesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.InstallNpmPackagesResponse:
        r"""Installs dependency NPM packages (inside a
        Workspace).

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_install_npm_packages():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.InstallNpmPackagesRequest(
                    workspace="workspace_value",
                )

                # Make the request
                response = await client.install_npm_packages(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.InstallNpmPackagesRequest, dict]):
                The request object. `InstallNpmPackages` request
                message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.InstallNpmPackagesResponse:
                InstallNpmPackages response message.
        """
        # Create or coerce a protobuf request object.
        request = dataform.InstallNpmPackagesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.install_npm_packages,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    async def pull_git_commits(
        self,
        request: Union[dataform.PullGitCommitsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Pulls Git commits from the Repository's remote into a
        Workspace.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_pull_git_commits():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                author = dataform_v1alpha2.CommitAuthor()
                author.name = "name_value"
                author.email_address = "email_address_value"

                request = dataform_v1alpha2.PullGitCommitsRequest(
                    name="name_value",
                    author=author,
                )

                # Make the request
                await client.pull_git_commits(request=request)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.PullGitCommitsRequest, dict]):
                The request object. `PullGitCommits` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = dataform.PullGitCommitsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.pull_git_commits,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def push_git_commits(
        self,
        request: Union[dataform.PushGitCommitsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Pushes Git commits from a Workspace to the
        Repository's remote.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_push_git_commits():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.PushGitCommitsRequest(
                    name="name_value",
                )

                # Make the request
                await client.push_git_commits(request=request)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.PushGitCommitsRequest, dict]):
                The request object. `PushGitCommits` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = dataform.PushGitCommitsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.push_git_commits,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def fetch_file_git_statuses(
        self,
        request: Union[dataform.FetchFileGitStatusesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.FetchFileGitStatusesResponse:
        r"""Fetches Git statuses for the files in a Workspace.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_fetch_file_git_statuses():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.FetchFileGitStatusesRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.fetch_file_git_statuses(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.FetchFileGitStatusesRequest, dict]):
                The request object. `FetchFileGitStatuses` request
                message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.FetchFileGitStatusesResponse:
                FetchFileGitStatuses response message.
        """
        # Create or coerce a protobuf request object.
        request = dataform.FetchFileGitStatusesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.fetch_file_git_statuses,
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

        # Done; return the response.
        return response

    async def fetch_git_ahead_behind(
        self,
        request: Union[dataform.FetchGitAheadBehindRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.FetchGitAheadBehindResponse:
        r"""Fetches Git ahead/behind against a remote branch.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_fetch_git_ahead_behind():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.FetchGitAheadBehindRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.fetch_git_ahead_behind(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.FetchGitAheadBehindRequest, dict]):
                The request object. `FetchGitAheadBehind` request
                message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.FetchGitAheadBehindResponse:
                FetchGitAheadBehind response message.
        """
        # Create or coerce a protobuf request object.
        request = dataform.FetchGitAheadBehindRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.fetch_git_ahead_behind,
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

        # Done; return the response.
        return response

    async def commit_workspace_changes(
        self,
        request: Union[dataform.CommitWorkspaceChangesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Applies a Git commit for uncommitted files in a
        Workspace.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_commit_workspace_changes():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                author = dataform_v1alpha2.CommitAuthor()
                author.name = "name_value"
                author.email_address = "email_address_value"

                request = dataform_v1alpha2.CommitWorkspaceChangesRequest(
                    name="name_value",
                    author=author,
                )

                # Make the request
                await client.commit_workspace_changes(request=request)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.CommitWorkspaceChangesRequest, dict]):
                The request object. `CommitWorkspaceChanges` request
                message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = dataform.CommitWorkspaceChangesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.commit_workspace_changes,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def reset_workspace_changes(
        self,
        request: Union[dataform.ResetWorkspaceChangesRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Performs a Git reset for uncommitted files in a
        Workspace.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_reset_workspace_changes():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.ResetWorkspaceChangesRequest(
                    name="name_value",
                )

                # Make the request
                await client.reset_workspace_changes(request=request)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.ResetWorkspaceChangesRequest, dict]):
                The request object. `ResetWorkspaceChanges` request
                message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = dataform.ResetWorkspaceChangesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.reset_workspace_changes,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def fetch_file_diff(
        self,
        request: Union[dataform.FetchFileDiffRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.FetchFileDiffResponse:
        r"""Fetches Git diff for an uncommitted file in a
        Workspace.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_fetch_file_diff():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.FetchFileDiffRequest(
                    workspace="workspace_value",
                    path="path_value",
                )

                # Make the request
                response = await client.fetch_file_diff(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.FetchFileDiffRequest, dict]):
                The request object. `FetchFileDiff` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.FetchFileDiffResponse:
                FetchFileDiff response message.
        """
        # Create or coerce a protobuf request object.
        request = dataform.FetchFileDiffRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.fetch_file_diff,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    async def query_directory_contents(
        self,
        request: Union[dataform.QueryDirectoryContentsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.QueryDirectoryContentsAsyncPager:
        r"""Returns the contents of a given Workspace directory.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_query_directory_contents():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.QueryDirectoryContentsRequest(
                    workspace="workspace_value",
                )

                # Make the request
                page_result = client.query_directory_contents(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.QueryDirectoryContentsRequest, dict]):
                The request object. `QueryDirectoryContents` request
                message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.services.dataform.pagers.QueryDirectoryContentsAsyncPager:
                QueryDirectoryContents response message.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = dataform.QueryDirectoryContentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.query_directory_contents,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
            ),
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
        response = pagers.QueryDirectoryContentsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def make_directory(
        self,
        request: Union[dataform.MakeDirectoryRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.MakeDirectoryResponse:
        r"""Creates a directory inside a Workspace.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_make_directory():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.MakeDirectoryRequest(
                    workspace="workspace_value",
                    path="path_value",
                )

                # Make the request
                response = await client.make_directory(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.MakeDirectoryRequest, dict]):
                The request object. `MakeDirectory` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.MakeDirectoryResponse:
                MakeDirectory response message.
        """
        # Create or coerce a protobuf request object.
        request = dataform.MakeDirectoryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.make_directory,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    async def remove_directory(
        self,
        request: Union[dataform.RemoveDirectoryRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a directory (inside a Workspace) and all of
        its contents.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_remove_directory():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.RemoveDirectoryRequest(
                    workspace="workspace_value",
                    path="path_value",
                )

                # Make the request
                await client.remove_directory(request=request)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.RemoveDirectoryRequest, dict]):
                The request object. `RemoveDirectory` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = dataform.RemoveDirectoryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.remove_directory,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
            ),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def move_directory(
        self,
        request: Union[dataform.MoveDirectoryRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.MoveDirectoryResponse:
        r"""Moves a directory (inside a Workspace), and all of
        its contents, to a new location.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_move_directory():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.MoveDirectoryRequest(
                    workspace="workspace_value",
                    path="path_value",
                    new_path="new_path_value",
                )

                # Make the request
                response = await client.move_directory(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.MoveDirectoryRequest, dict]):
                The request object. `MoveDirectory` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.MoveDirectoryResponse:
                MoveDirectory response message.
        """
        # Create or coerce a protobuf request object.
        request = dataform.MoveDirectoryRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.move_directory,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    async def read_file(
        self,
        request: Union[dataform.ReadFileRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.ReadFileResponse:
        r"""Returns the contents of a file (inside a Workspace).

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_read_file():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.ReadFileRequest(
                    workspace="workspace_value",
                    path="path_value",
                )

                # Make the request
                response = await client.read_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.ReadFileRequest, dict]):
                The request object. `ReadFile` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.ReadFileResponse:
                ReadFile response message.
        """
        # Create or coerce a protobuf request object.
        request = dataform.ReadFileRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.read_file,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    async def remove_file(
        self,
        request: Union[dataform.RemoveFileRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a file (inside a Workspace).

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_remove_file():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.RemoveFileRequest(
                    workspace="workspace_value",
                    path="path_value",
                )

                # Make the request
                await client.remove_file(request=request)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.RemoveFileRequest, dict]):
                The request object. `RemoveFile` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = dataform.RemoveFileRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.remove_file,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
            ),
        )

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def move_file(
        self,
        request: Union[dataform.MoveFileRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.MoveFileResponse:
        r"""Moves a file (inside a Workspace) to a new location.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_move_file():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.MoveFileRequest(
                    workspace="workspace_value",
                    path="path_value",
                    new_path="new_path_value",
                )

                # Make the request
                response = await client.move_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.MoveFileRequest, dict]):
                The request object. `MoveFile` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.MoveFileResponse:
                MoveFile response message.
        """
        # Create or coerce a protobuf request object.
        request = dataform.MoveFileRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.move_file,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    async def write_file(
        self,
        request: Union[dataform.WriteFileRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.WriteFileResponse:
        r"""Writes to a file (inside a Workspace).

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_write_file():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.WriteFileRequest(
                    workspace="workspace_value",
                    path="path_value",
                    contents=b'contents_blob',
                )

                # Make the request
                response = await client.write_file(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.WriteFileRequest, dict]):
                The request object. `WriteFile` request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.WriteFileResponse:
                WriteFile response message.
        """
        # Create or coerce a protobuf request object.
        request = dataform.WriteFileRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.write_file,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("workspace", request.workspace),)
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

    async def list_compilation_results(
        self,
        request: Union[dataform.ListCompilationResultsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCompilationResultsAsyncPager:
        r"""Lists CompilationResults in a given Repository.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_list_compilation_results():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.ListCompilationResultsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_compilation_results(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.ListCompilationResultsRequest, dict]):
                The request object. `ListCompilationResults` request
                message.
            parent (:class:`str`):
                Required. The repository in which to list compilation
                results. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.services.dataform.pagers.ListCompilationResultsAsyncPager:
                ListCompilationResults response message.

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

        request = dataform.ListCompilationResultsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_compilation_results,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListCompilationResultsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_compilation_result(
        self,
        request: Union[dataform.GetCompilationResultRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.CompilationResult:
        r"""Fetches a single CompilationResult.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_get_compilation_result():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.GetCompilationResultRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_compilation_result(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.GetCompilationResultRequest, dict]):
                The request object. `GetCompilationResult` request
                message.
            name (:class:`str`):
                Required. The compilation result's
                name.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.CompilationResult:
                Represents the result of compiling a
                Dataform project.

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

        request = dataform.GetCompilationResultRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_compilation_result,
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

        # Done; return the response.
        return response

    async def create_compilation_result(
        self,
        request: Union[dataform.CreateCompilationResultRequest, dict] = None,
        *,
        parent: str = None,
        compilation_result: dataform.CompilationResult = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.CompilationResult:
        r"""Creates a new CompilationResult in a given project
        and location.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_create_compilation_result():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                compilation_result = dataform_v1alpha2.CompilationResult()
                compilation_result.git_commitish = "git_commitish_value"

                request = dataform_v1alpha2.CreateCompilationResultRequest(
                    parent="parent_value",
                    compilation_result=compilation_result,
                )

                # Make the request
                response = await client.create_compilation_result(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.CreateCompilationResultRequest, dict]):
                The request object. `CreateCompilationResult` request
                message.
            parent (:class:`str`):
                Required. The repository in which to create the
                compilation result. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            compilation_result (:class:`google.cloud.dataform_v1alpha2.types.CompilationResult`):
                Required. The compilation result to
                create.

                This corresponds to the ``compilation_result`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.CompilationResult:
                Represents the result of compiling a
                Dataform project.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, compilation_result])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = dataform.CreateCompilationResultRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if compilation_result is not None:
            request.compilation_result = compilation_result

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_compilation_result,
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

        # Done; return the response.
        return response

    async def query_compilation_result_actions(
        self,
        request: Union[dataform.QueryCompilationResultActionsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.QueryCompilationResultActionsAsyncPager:
        r"""Returns CompilationResultActions in a given
        CompilationResult.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_query_compilation_result_actions():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.QueryCompilationResultActionsRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.query_compilation_result_actions(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.QueryCompilationResultActionsRequest, dict]):
                The request object. `QueryCompilationResultActions`
                request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.services.dataform.pagers.QueryCompilationResultActionsAsyncPager:
                QueryCompilationResultActions response message.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = dataform.QueryCompilationResultActionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.query_compilation_result_actions,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.QueryCompilationResultActionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_workflow_invocations(
        self,
        request: Union[dataform.ListWorkflowInvocationsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListWorkflowInvocationsAsyncPager:
        r"""Lists WorkflowInvocations in a given Repository.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_list_workflow_invocations():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.ListWorkflowInvocationsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_workflow_invocations(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.ListWorkflowInvocationsRequest, dict]):
                The request object. `ListWorkflowInvocations` request
                message.
            parent (:class:`str`):
                Required. The parent resource of the WorkflowInvocation
                type. Must be in the format
                ``projects/*/locations/*/repositories/*``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.services.dataform.pagers.ListWorkflowInvocationsAsyncPager:
                ListWorkflowInvocations response message.

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

        request = dataform.ListWorkflowInvocationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_workflow_invocations,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListWorkflowInvocationsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_workflow_invocation(
        self,
        request: Union[dataform.GetWorkflowInvocationRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.WorkflowInvocation:
        r"""Fetches a single WorkflowInvocation.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_get_workflow_invocation():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.GetWorkflowInvocationRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_workflow_invocation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.GetWorkflowInvocationRequest, dict]):
                The request object. `GetWorkflowInvocation` request
                message.
            name (:class:`str`):
                Required. The workflow invocation
                resource's name.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.WorkflowInvocation:
                Represents a single invocation of a
                compilation result.

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

        request = dataform.GetWorkflowInvocationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_workflow_invocation,
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

        # Done; return the response.
        return response

    async def create_workflow_invocation(
        self,
        request: Union[dataform.CreateWorkflowInvocationRequest, dict] = None,
        *,
        parent: str = None,
        workflow_invocation: dataform.WorkflowInvocation = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataform.WorkflowInvocation:
        r"""Creates a new WorkflowInvocation in a given
        Repository.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_create_workflow_invocation():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.CreateWorkflowInvocationRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_workflow_invocation(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.CreateWorkflowInvocationRequest, dict]):
                The request object. `CreateWorkflowInvocation` request
                message.
            parent (:class:`str`):
                Required. The parent resource of the
                WorkflowInvocation type.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            workflow_invocation (:class:`google.cloud.dataform_v1alpha2.types.WorkflowInvocation`):
                Required. The workflow invocation
                resource to create.

                This corresponds to the ``workflow_invocation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.types.WorkflowInvocation:
                Represents a single invocation of a
                compilation result.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, workflow_invocation])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = dataform.CreateWorkflowInvocationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if workflow_invocation is not None:
            request.workflow_invocation = workflow_invocation

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_workflow_invocation,
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

        # Done; return the response.
        return response

    async def delete_workflow_invocation(
        self,
        request: Union[dataform.DeleteWorkflowInvocationRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a single WorkflowInvocation.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_delete_workflow_invocation():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.DeleteWorkflowInvocationRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_workflow_invocation(request=request)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.DeleteWorkflowInvocationRequest, dict]):
                The request object. `DeleteWorkflowInvocation` request
                message.
            name (:class:`str`):
                Required. The workflow invocation
                resource's name.

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

        request = dataform.DeleteWorkflowInvocationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_workflow_invocation,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def cancel_workflow_invocation(
        self,
        request: Union[dataform.CancelWorkflowInvocationRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Requests cancellation of a running
        WorkflowInvocation.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_cancel_workflow_invocation():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.CancelWorkflowInvocationRequest(
                    name="name_value",
                )

                # Make the request
                await client.cancel_workflow_invocation(request=request)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.CancelWorkflowInvocationRequest, dict]):
                The request object. `CancelWorkflowInvocation` request
                message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        request = dataform.CancelWorkflowInvocationRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_workflow_invocation,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def query_workflow_invocation_actions(
        self,
        request: Union[dataform.QueryWorkflowInvocationActionsRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.QueryWorkflowInvocationActionsAsyncPager:
        r"""Returns WorkflowInvocationActions in a given
        WorkflowInvocation.

        .. code-block:: python

            from google.cloud import dataform_v1alpha2

            async def sample_query_workflow_invocation_actions():
                # Create a client
                client = dataform_v1alpha2.DataformAsyncClient()

                # Initialize request argument(s)
                request = dataform_v1alpha2.QueryWorkflowInvocationActionsRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.query_workflow_invocation_actions(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.dataform_v1alpha2.types.QueryWorkflowInvocationActionsRequest, dict]):
                The request object. `QueryWorkflowInvocationActions`
                request message.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataform_v1alpha2.services.dataform.pagers.QueryWorkflowInvocationActionsAsyncPager:
                QueryWorkflowInvocationActions response message.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        request = dataform.QueryWorkflowInvocationActionsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.query_workflow_invocation_actions,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.QueryWorkflowInvocationActionsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the IAM access control policy on the specified function.

        Replaces any existing policy.

        Args:
            request (:class:`~.iam_policy_pb2.SetIamPolicyRequest`):
                The request object. Request message for `SetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**

                .. code-block:: python

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.set_iam_policy,
            default_timeout=None,
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

    async def get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the IAM access control policy for a function.

        Returns an empty policy if the function exists and does not have a
        policy set.

        Args:
            request (:class:`~.iam_policy_pb2.GetIamPolicyRequest`):
                The request object. Request message for `GetIamPolicy`
                method.
            retry (google.api_core.retry.Retry): Designation of what errors, if
                any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.
                A ``Policy`` is a collection of ``bindings``. A
                ``binding`` binds one or more ``members`` to a single
                ``role``. Members can be user accounts, service
                accounts, Google groups, and domains (such as G Suite).
                A ``role`` is a named list of permissions (defined by
                IAM or configured by users). A ``binding`` can
                optionally specify a ``condition``, which is a logic
                expression that further constrains the role binding
                based on attributes about the request and/or target
                resource.

                **JSON Example**

                .. code-block:: python

                    {
                      "bindings": [
                        {
                          "role": "roles/resourcemanager.organizationAdmin",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                          ]
                        },
                        {
                          "role": "roles/resourcemanager.organizationViewer",
                          "members": ["user:eve@example.com"],
                          "condition": {
                            "title": "expirable access",
                            "description": "Does not grant access after Sep 2020",
                            "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')",
                          }
                        }
                      ]
                    }

                **YAML Example**

                ::

                    bindings:
                    - members:
                      - user:mike@example.com
                      - group:admins@example.com
                      - domain:google.com
                      - serviceAccount:my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin
                    - members:
                      - user:eve@example.com
                      role: roles/resourcemanager.organizationViewer
                      condition:
                        title: expirable access
                        description: Does not grant access after Sep 2020
                        expression: request.time < timestamp('2020-10-01T00:00:00.000Z')

                For a description of IAM and its features, see the `IAM
                developer's
                guide <https://cloud.google.com/iam/docs>`__.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.get_iam_policy,
            default_timeout=None,
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
        request: iam_policy_pb2.TestIamPermissionsRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Tests the specified IAM permissions against the IAM access control
            policy for a function.

        If the function does not exist, this will return an empty set
        of permissions, not a NOT_FOUND error.

        Args:
            request (:class:`~.iam_policy_pb2.TestIamPermissionsRequest`):
                The request object. Request message for
                `TestIamPermissions` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for ``TestIamPermissions`` method.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.test_iam_permissions,
            default_timeout=None,
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

    async def get_location(
        self,
        request: locations_pb2.GetLocationRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.Location:
        r"""Gets information about a location.

        Args:
            request (:class:`~.location_pb2.GetLocationRequest`):
                The request object. Request message for
                `GetLocation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.Location:
                Location object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.GetLocationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.get_location,
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

        # Done; return the response.
        return response

    async def list_locations(
        self,
        request: locations_pb2.ListLocationsRequest = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> locations_pb2.ListLocationsResponse:
        r"""Lists information about the supported locations for this service.

        Args:
            request (:class:`~.location_pb2.ListLocationsRequest`):
                The request object. Request message for
                `ListLocations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                 if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.location_pb2.ListLocationsResponse:
                Response message for ``ListLocations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = locations_pb2.ListLocationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._client._transport.list_locations,
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

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-dataform",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DataformAsyncClient",)
