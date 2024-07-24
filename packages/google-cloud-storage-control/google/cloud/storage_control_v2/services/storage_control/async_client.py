# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from typing import (
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)
import uuid

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.storage_control_v2 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.storage_control_v2.services.storage_control import pagers
from google.cloud.storage_control_v2.types import storage_control

from .client import StorageControlClient
from .transports.base import DEFAULT_CLIENT_INFO, StorageControlTransport
from .transports.grpc_asyncio import StorageControlGrpcAsyncIOTransport


class StorageControlAsyncClient:
    """StorageControl service includes selected control plane
    operations.
    """

    _client: StorageControlClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = StorageControlClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = StorageControlClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = StorageControlClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = StorageControlClient._DEFAULT_UNIVERSE

    folder_path = staticmethod(StorageControlClient.folder_path)
    parse_folder_path = staticmethod(StorageControlClient.parse_folder_path)
    managed_folder_path = staticmethod(StorageControlClient.managed_folder_path)
    parse_managed_folder_path = staticmethod(
        StorageControlClient.parse_managed_folder_path
    )
    storage_layout_path = staticmethod(StorageControlClient.storage_layout_path)
    parse_storage_layout_path = staticmethod(
        StorageControlClient.parse_storage_layout_path
    )
    common_billing_account_path = staticmethod(
        StorageControlClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        StorageControlClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(StorageControlClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        StorageControlClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        StorageControlClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        StorageControlClient.parse_common_organization_path
    )
    common_project_path = staticmethod(StorageControlClient.common_project_path)
    parse_common_project_path = staticmethod(
        StorageControlClient.parse_common_project_path
    )
    common_location_path = staticmethod(StorageControlClient.common_location_path)
    parse_common_location_path = staticmethod(
        StorageControlClient.parse_common_location_path
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
            StorageControlAsyncClient: The constructed client.
        """
        return StorageControlClient.from_service_account_info.__func__(StorageControlAsyncClient, info, *args, **kwargs)  # type: ignore

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
            StorageControlAsyncClient: The constructed client.
        """
        return StorageControlClient.from_service_account_file.__func__(StorageControlAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return StorageControlClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> StorageControlTransport:
        """Returns the transport used by the client instance.

        Returns:
            StorageControlTransport: The transport used by the client instance.
        """
        return self._client.transport

    @property
    def api_endpoint(self):
        """Return the API endpoint used by the client instance.

        Returns:
            str: The API endpoint used by the client instance.
        """
        return self._client._api_endpoint

    @property
    def universe_domain(self) -> str:
        """Return the universe domain used by the client instance.

        Returns:
            str: The universe domain used
                by the client instance.
        """
        return self._client._universe_domain

    get_transport_class = functools.partial(
        type(StorageControlClient).get_transport_class, type(StorageControlClient)
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[str, StorageControlTransport, Callable[..., StorageControlTransport]]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the storage control async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,StorageControlTransport,Callable[..., StorageControlTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the StorageControlTransport constructor.
                If set to None, a transport is chosen automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]):
                Custom options for the client.

                1. The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client when ``transport`` is
                not explicitly provided. Only if this property is not set and
                ``transport`` was not explicitly provided, the endpoint is
                determined by the GOOGLE_API_USE_MTLS_ENDPOINT environment
                variable, which have one of the following values:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto-switch to the
                default mTLS endpoint if client certificate is present; this is
                the default value).

                2. If the GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide a client certificate for mTLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

                3. The ``universe_domain`` property can be used to override the
                default "googleapis.com" universe. Note that ``api_endpoint``
                property still takes precedence; and ``universe_domain`` is
                currently not supported for mTLS.

            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = StorageControlClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_folder(
        self,
        request: Optional[Union[storage_control.CreateFolderRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        folder: Optional[storage_control.Folder] = None,
        folder_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage_control.Folder:
        r"""Creates a new folder. This operation is only
        applicable to a hierarchical namespace enabled bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_control_v2

            async def sample_create_folder():
                # Create a client
                client = storage_control_v2.StorageControlAsyncClient()

                # Initialize request argument(s)
                request = storage_control_v2.CreateFolderRequest(
                    parent="parent_value",
                    folder_id="folder_id_value",
                )

                # Make the request
                response = await client.create_folder(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.storage_control_v2.types.CreateFolderRequest, dict]]):
                The request object. Request message for CreateFolder.
                This operation is only applicable to a
                hierarchical namespace enabled bucket.
            parent (:class:`str`):
                Required. Name of the bucket in which
                the folder will reside. The bucket must
                be a hierarchical namespace enabled
                bucket.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            folder (:class:`google.cloud.storage_control_v2.types.Folder`):
                Required. Properties of the new folder being created.
                The bucket and name of the folder are specified in the
                parent and folder_id fields, respectively. Populating
                those fields in ``folder`` will result in an error.

                This corresponds to the ``folder`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            folder_id (:class:`str`):
                Required. The full name of a folder, including all its
                parent folders. Folders use single '/' characters as a
                delimiter. The folder_id must end with a slash. For
                example, the folder_id of "books/biographies/" would
                create a new "biographies/" folder under the "books/"
                folder.

                This corresponds to the ``folder_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_control_v2.types.Folder:
                A folder resource. This resource can
                only exist in a hierarchical namespace
                enabled bucket.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, folder, folder_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, storage_control.CreateFolderRequest):
            request = storage_control.CreateFolderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if folder is not None:
            request.folder = folder
        if folder_id is not None:
            request.folder_id = folder_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.create_folder
        ]

        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_folder(
        self,
        request: Optional[Union[storage_control.DeleteFolderRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Permanently deletes an empty folder. This operation
        is only applicable to a hierarchical namespace enabled
        bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_control_v2

            async def sample_delete_folder():
                # Create a client
                client = storage_control_v2.StorageControlAsyncClient()

                # Initialize request argument(s)
                request = storage_control_v2.DeleteFolderRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_folder(request=request)

        Args:
            request (Optional[Union[google.cloud.storage_control_v2.types.DeleteFolderRequest, dict]]):
                The request object. Request message for DeleteFolder.
                This operation is only applicable to a
                hierarchical namespace enabled bucket.
            name (:class:`str`):
                Required. Name of the folder. Format:
                ``projects/{project}/buckets/{bucket}/folders/{folder}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, storage_control.DeleteFolderRequest):
            request = storage_control.DeleteFolderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.delete_folder
        ]

        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def get_folder(
        self,
        request: Optional[Union[storage_control.GetFolderRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage_control.Folder:
        r"""Returns metadata for the specified folder. This
        operation is only applicable to a hierarchical namespace
        enabled bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_control_v2

            async def sample_get_folder():
                # Create a client
                client = storage_control_v2.StorageControlAsyncClient()

                # Initialize request argument(s)
                request = storage_control_v2.GetFolderRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_folder(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.storage_control_v2.types.GetFolderRequest, dict]]):
                The request object. Request message for GetFolder. This
                operation is only applicable to a
                hierarchical namespace enabled bucket.
            name (:class:`str`):
                Required. Name of the folder. Format:
                ``projects/{project}/buckets/{bucket}/folders/{folder}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_control_v2.types.Folder:
                A folder resource. This resource can
                only exist in a hierarchical namespace
                enabled bucket.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, storage_control.GetFolderRequest):
            request = storage_control.GetFolderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.get_folder
        ]

        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_folders(
        self,
        request: Optional[Union[storage_control.ListFoldersRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListFoldersAsyncPager:
        r"""Retrieves a list of folders. This operation is only
        applicable to a hierarchical namespace enabled bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_control_v2

            async def sample_list_folders():
                # Create a client
                client = storage_control_v2.StorageControlAsyncClient()

                # Initialize request argument(s)
                request = storage_control_v2.ListFoldersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_folders(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.storage_control_v2.types.ListFoldersRequest, dict]]):
                The request object. Request message for ListFolders. This
                operation is only applicable to a
                hierarchical namespace enabled bucket.
            parent (:class:`str`):
                Required. Name of the bucket in which
                to look for folders. The bucket must be
                a hierarchical namespace enabled bucket.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_control_v2.services.storage_control.pagers.ListFoldersAsyncPager:
                Response message for ListFolders.

                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, storage_control.ListFoldersRequest):
            request = storage_control.ListFoldersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_folders
        ]

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListFoldersAsyncPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def rename_folder(
        self,
        request: Optional[Union[storage_control.RenameFolderRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        destination_folder_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Renames a source folder to a destination folder. This
        operation is only applicable to a hierarchical namespace
        enabled bucket. During a rename, the source and
        destination folders are locked until the long running
        operation completes.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_control_v2

            async def sample_rename_folder():
                # Create a client
                client = storage_control_v2.StorageControlAsyncClient()

                # Initialize request argument(s)
                request = storage_control_v2.RenameFolderRequest(
                    name="name_value",
                    destination_folder_id="destination_folder_id_value",
                )

                # Make the request
                operation = client.rename_folder(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.storage_control_v2.types.RenameFolderRequest, dict]]):
                The request object. Request message for RenameFolder.
                This operation is only applicable to a
                hierarchical namespace enabled bucket.
            name (:class:`str`):
                Required. Name of the source folder being renamed.
                Format:
                ``projects/{project}/buckets/{bucket}/folders/{folder}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            destination_folder_id (:class:`str`):
                Required. The destination folder ID, e.g. ``foo/bar/``.
                This corresponds to the ``destination_folder_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.storage_control_v2.types.Folder` A folder resource. This resource can only exist in a hierarchical namespace
                   enabled bucket.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, destination_folder_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, storage_control.RenameFolderRequest):
            request = storage_control.RenameFolderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if destination_folder_id is not None:
            request.destination_folder_id = destination_folder_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.rename_folder
        ]

        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        # Validate the universe domain.
        self._client._validate_universe_domain()

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
            storage_control.Folder,
            metadata_type=storage_control.RenameFolderMetadata,
        )

        # Done; return the response.
        return response

    async def get_storage_layout(
        self,
        request: Optional[Union[storage_control.GetStorageLayoutRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage_control.StorageLayout:
        r"""Returns the storage layout configuration for a given
        bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_control_v2

            async def sample_get_storage_layout():
                # Create a client
                client = storage_control_v2.StorageControlAsyncClient()

                # Initialize request argument(s)
                request = storage_control_v2.GetStorageLayoutRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_storage_layout(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.storage_control_v2.types.GetStorageLayoutRequest, dict]]):
                The request object. Request message for GetStorageLayout.
            name (:class:`str`):
                Required. The name of the StorageLayout resource.
                Format:
                ``projects/{project}/buckets/{bucket}/storageLayout``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_control_v2.types.StorageLayout:
                The storage layout configuration of a
                bucket.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, storage_control.GetStorageLayoutRequest):
            request = storage_control.GetStorageLayoutRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.get_storage_layout
        ]

        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_managed_folder(
        self,
        request: Optional[
            Union[storage_control.CreateManagedFolderRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        managed_folder: Optional[storage_control.ManagedFolder] = None,
        managed_folder_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage_control.ManagedFolder:
        r"""Creates a new managed folder.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_control_v2

            async def sample_create_managed_folder():
                # Create a client
                client = storage_control_v2.StorageControlAsyncClient()

                # Initialize request argument(s)
                request = storage_control_v2.CreateManagedFolderRequest(
                    parent="parent_value",
                    managed_folder_id="managed_folder_id_value",
                )

                # Make the request
                response = await client.create_managed_folder(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.storage_control_v2.types.CreateManagedFolderRequest, dict]]):
                The request object. Request message for
                CreateManagedFolder.
            parent (:class:`str`):
                Required. Name of the bucket this
                managed folder belongs to.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            managed_folder (:class:`google.cloud.storage_control_v2.types.ManagedFolder`):
                Required. Properties of the managed folder being
                created. The bucket and managed folder names are
                specified in the ``parent`` and ``managed_folder_id``
                fields. Populating these fields in ``managed_folder``
                will result in an error.

                This corresponds to the ``managed_folder`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            managed_folder_id (:class:`str`):
                Required. The name of the managed folder. It uses a
                single ``/`` as delimiter and leading and trailing ``/``
                are allowed.

                This corresponds to the ``managed_folder_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_control_v2.types.ManagedFolder:
                A managed folder.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, managed_folder, managed_folder_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, storage_control.CreateManagedFolderRequest):
            request = storage_control.CreateManagedFolderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if managed_folder is not None:
            request.managed_folder = managed_folder
        if managed_folder_id is not None:
            request.managed_folder_id = managed_folder_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.create_managed_folder
        ]

        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_managed_folder(
        self,
        request: Optional[
            Union[storage_control.DeleteManagedFolderRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Permanently deletes an empty managed folder.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_control_v2

            async def sample_delete_managed_folder():
                # Create a client
                client = storage_control_v2.StorageControlAsyncClient()

                # Initialize request argument(s)
                request = storage_control_v2.DeleteManagedFolderRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_managed_folder(request=request)

        Args:
            request (Optional[Union[google.cloud.storage_control_v2.types.DeleteManagedFolderRequest, dict]]):
                The request object. DeleteManagedFolder RPC request
                message.
            name (:class:`str`):
                Required. Name of the managed folder. Format:
                ``projects/{project}/buckets/{bucket}/managedFolders/{managedFolder}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, storage_control.DeleteManagedFolderRequest):
            request = storage_control.DeleteManagedFolderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.delete_managed_folder
        ]

        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def get_managed_folder(
        self,
        request: Optional[Union[storage_control.GetManagedFolderRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> storage_control.ManagedFolder:
        r"""Returns metadata for the specified managed folder.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_control_v2

            async def sample_get_managed_folder():
                # Create a client
                client = storage_control_v2.StorageControlAsyncClient()

                # Initialize request argument(s)
                request = storage_control_v2.GetManagedFolderRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_managed_folder(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.storage_control_v2.types.GetManagedFolderRequest, dict]]):
                The request object. Request message for GetManagedFolder.
            name (:class:`str`):
                Required. Name of the managed folder. Format:
                ``projects/{project}/buckets/{bucket}/managedFolders/{managedFolder}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_control_v2.types.ManagedFolder:
                A managed folder.
        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, storage_control.GetManagedFolderRequest):
            request = storage_control.GetManagedFolderRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.get_managed_folder
        ]

        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_managed_folders(
        self,
        request: Optional[
            Union[storage_control.ListManagedFoldersRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListManagedFoldersAsyncPager:
        r"""Retrieves a list of managed folders for a given
        bucket.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import storage_control_v2

            async def sample_list_managed_folders():
                # Create a client
                client = storage_control_v2.StorageControlAsyncClient()

                # Initialize request argument(s)
                request = storage_control_v2.ListManagedFoldersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_managed_folders(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.storage_control_v2.types.ListManagedFoldersRequest, dict]]):
                The request object. Request message for
                ListManagedFolders.
            parent (:class:`str`):
                Required. Name of the bucket this
                managed folder belongs to.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.storage_control_v2.services.storage_control.pagers.ListManagedFoldersAsyncPager:
                Response message for
                ListManagedFolders.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, storage_control.ListManagedFoldersRequest):
            request = storage_control.ListManagedFoldersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_managed_folders
        ]

        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        response = await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListManagedFoldersAsyncPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self) -> "StorageControlAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("StorageControlAsyncClient",)
