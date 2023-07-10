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
)

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.maps.mapsplatformdatasets_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.maps.mapsplatformdatasets_v1.services.maps_platform_datasets import pagers
from google.maps.mapsplatformdatasets_v1.types import data_source
from google.maps.mapsplatformdatasets_v1.types import dataset
from google.maps.mapsplatformdatasets_v1.types import dataset as gmm_dataset
from google.maps.mapsplatformdatasets_v1.types import maps_platform_datasets

from .client import MapsPlatformDatasetsClient
from .transports.base import DEFAULT_CLIENT_INFO, MapsPlatformDatasetsTransport
from .transports.grpc_asyncio import MapsPlatformDatasetsGrpcAsyncIOTransport


class MapsPlatformDatasetsAsyncClient:
    """Service definition for the Maps Platform Datasets API."""

    _client: MapsPlatformDatasetsClient

    DEFAULT_ENDPOINT = MapsPlatformDatasetsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = MapsPlatformDatasetsClient.DEFAULT_MTLS_ENDPOINT

    dataset_path = staticmethod(MapsPlatformDatasetsClient.dataset_path)
    parse_dataset_path = staticmethod(MapsPlatformDatasetsClient.parse_dataset_path)
    common_billing_account_path = staticmethod(
        MapsPlatformDatasetsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        MapsPlatformDatasetsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(MapsPlatformDatasetsClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        MapsPlatformDatasetsClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        MapsPlatformDatasetsClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        MapsPlatformDatasetsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(MapsPlatformDatasetsClient.common_project_path)
    parse_common_project_path = staticmethod(
        MapsPlatformDatasetsClient.parse_common_project_path
    )
    common_location_path = staticmethod(MapsPlatformDatasetsClient.common_location_path)
    parse_common_location_path = staticmethod(
        MapsPlatformDatasetsClient.parse_common_location_path
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
            MapsPlatformDatasetsAsyncClient: The constructed client.
        """
        return MapsPlatformDatasetsClient.from_service_account_info.__func__(MapsPlatformDatasetsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            MapsPlatformDatasetsAsyncClient: The constructed client.
        """
        return MapsPlatformDatasetsClient.from_service_account_file.__func__(MapsPlatformDatasetsAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return MapsPlatformDatasetsClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> MapsPlatformDatasetsTransport:
        """Returns the transport used by the client instance.

        Returns:
            MapsPlatformDatasetsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(MapsPlatformDatasetsClient).get_transport_class,
        type(MapsPlatformDatasetsClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, MapsPlatformDatasetsTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the maps platform datasets client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.MapsPlatformDatasetsTransport]): The
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
        self._client = MapsPlatformDatasetsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_dataset(
        self,
        request: Optional[
            Union[maps_platform_datasets.CreateDatasetRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        dataset: Optional[gmm_dataset.Dataset] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gmm_dataset.Dataset:
        r"""Create a new dataset for the specified project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.maps import mapsplatformdatasets_v1

            async def sample_create_dataset():
                # Create a client
                client = mapsplatformdatasets_v1.MapsPlatformDatasetsAsyncClient()

                # Initialize request argument(s)
                request = mapsplatformdatasets_v1.CreateDatasetRequest(
                    parent="parent_value",
                )

                # Make the request
                response = await client.create_dataset(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.maps.mapsplatformdatasets_v1.types.CreateDatasetRequest, dict]]):
                The request object. Request to create a maps dataset.
            parent (:class:`str`):
                Required. Parent project that will
                own the dataset. Format:
                projects/{$project}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            dataset (:class:`google.maps.mapsplatformdatasets_v1.types.Dataset`):
                Required. The dataset version to
                create.

                This corresponds to the ``dataset`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.maps.mapsplatformdatasets_v1.types.Dataset:
                A representation of a Maps Dataset
                resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, dataset])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = maps_platform_datasets.CreateDatasetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if dataset is not None:
            request.dataset = dataset

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_dataset,
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

        # Done; return the response.
        return response

    async def update_dataset_metadata(
        self,
        request: Optional[
            Union[maps_platform_datasets.UpdateDatasetMetadataRequest, dict]
        ] = None,
        *,
        dataset: Optional[gmm_dataset.Dataset] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gmm_dataset.Dataset:
        r"""Update the metadata for the dataset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.maps import mapsplatformdatasets_v1

            async def sample_update_dataset_metadata():
                # Create a client
                client = mapsplatformdatasets_v1.MapsPlatformDatasetsAsyncClient()

                # Initialize request argument(s)
                request = mapsplatformdatasets_v1.UpdateDatasetMetadataRequest(
                )

                # Make the request
                response = await client.update_dataset_metadata(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.maps.mapsplatformdatasets_v1.types.UpdateDatasetMetadataRequest, dict]]):
                The request object. Request to update the metadata fields
                of the dataset.
            dataset (:class:`google.maps.mapsplatformdatasets_v1.types.Dataset`):
                Required. The dataset to update. The dataset's name is
                used to identify the dataset to be updated. The name has
                the format: projects/{project}/datasets/{dataset_id}

                This corresponds to the ``dataset`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                The list of fields to be updated. Support the value "*"
                for full replacement.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.maps.mapsplatformdatasets_v1.types.Dataset:
                A representation of a Maps Dataset
                resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([dataset, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = maps_platform_datasets.UpdateDatasetMetadataRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if dataset is not None:
            request.dataset = dataset
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_dataset_metadata,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("dataset.name", request.dataset.name),)
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

    async def get_dataset(
        self,
        request: Optional[Union[maps_platform_datasets.GetDatasetRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dataset.Dataset:
        r"""Get the dataset.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.maps import mapsplatformdatasets_v1

            async def sample_get_dataset():
                # Create a client
                client = mapsplatformdatasets_v1.MapsPlatformDatasetsAsyncClient()

                # Initialize request argument(s)
                request = mapsplatformdatasets_v1.GetDatasetRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_dataset(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.maps.mapsplatformdatasets_v1.types.GetDatasetRequest, dict]]):
                The request object. Request to get the specified dataset.
            name (:class:`str`):
                Required. Resource name.
                projects/{project}/datasets/{dataset_id}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.maps.mapsplatformdatasets_v1.types.Dataset:
                A representation of a Maps Dataset
                resource.

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

        request = maps_platform_datasets.GetDatasetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_dataset,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
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

    async def list_datasets(
        self,
        request: Optional[
            Union[maps_platform_datasets.ListDatasetsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDatasetsAsyncPager:
        r"""List all the datasets for the specified project.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.maps import mapsplatformdatasets_v1

            async def sample_list_datasets():
                # Create a client
                client = mapsplatformdatasets_v1.MapsPlatformDatasetsAsyncClient()

                # Initialize request argument(s)
                request = mapsplatformdatasets_v1.ListDatasetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_datasets(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.maps.mapsplatformdatasets_v1.types.ListDatasetsRequest, dict]]):
                The request object. Request to list datasets for the
                project.
            parent (:class:`str`):
                Required. The name of the project to
                list all the datasets for.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.maps.mapsplatformdatasets_v1.services.maps_platform_datasets.pagers.ListDatasetsAsyncPager:
                Response to list datasets for the
                project.
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

        request = maps_platform_datasets.ListDatasetsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_datasets,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=10.0,
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
        response = pagers.ListDatasetsAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_dataset(
        self,
        request: Optional[
            Union[maps_platform_datasets.DeleteDatasetRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Delete the specified dataset .

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.maps import mapsplatformdatasets_v1

            async def sample_delete_dataset():
                # Create a client
                client = mapsplatformdatasets_v1.MapsPlatformDatasetsAsyncClient()

                # Initialize request argument(s)
                request = mapsplatformdatasets_v1.DeleteDatasetRequest(
                    name="name_value",
                )

                # Make the request
                await client.delete_dataset(request=request)

        Args:
            request (Optional[Union[google.maps.mapsplatformdatasets_v1.types.DeleteDatasetRequest, dict]]):
                The request object. Request to delete a dataset.
                The dataset to be deleted.
            name (:class:`str`):
                Required. Format:
                projects/${project}/datasets/{dataset_id}

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

        request = maps_platform_datasets.DeleteDatasetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_dataset,
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
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def __aenter__(self) -> "MapsPlatformDatasetsAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("MapsPlatformDatasetsAsyncClient",)
