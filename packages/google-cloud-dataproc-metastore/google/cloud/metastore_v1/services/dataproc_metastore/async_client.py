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
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.metastore_v1.services.dataproc_metastore import pagers
from google.cloud.metastore_v1.types import metastore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import DataprocMetastoreTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import DataprocMetastoreGrpcAsyncIOTransport
from .client import DataprocMetastoreClient


class DataprocMetastoreAsyncClient:
    """Configures and manages metastore services. Metastore services are
    fully managed, highly available, auto-scaled, auto-healing,
    OSS-native deployments of technical metadata management software.
    Each metastore service exposes a network endpoint through which
    metadata queries are served. Metadata queries can originate from a
    variety of sources, including Apache Hive, Apache Presto, and Apache
    Spark.

    The Dataproc Metastore API defines the following resource model:

    -  The service works with a collection of Google Cloud projects,
       named: ``/projects/*``

    -  Each project has a collection of available locations, named:
       ``/locations/*`` (a location must refer to a Google Cloud
       ``region``)

    -  Each location has a collection of services, named:
       ``/services/*``

    -  Dataproc Metastore services are resources with names of the form:

       ``/projects/{project_number}/locations/{location_id}/services/{service_id}``.
    """

    _client: DataprocMetastoreClient

    DEFAULT_ENDPOINT = DataprocMetastoreClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = DataprocMetastoreClient.DEFAULT_MTLS_ENDPOINT

    metadata_import_path = staticmethod(DataprocMetastoreClient.metadata_import_path)
    parse_metadata_import_path = staticmethod(
        DataprocMetastoreClient.parse_metadata_import_path
    )
    network_path = staticmethod(DataprocMetastoreClient.network_path)
    parse_network_path = staticmethod(DataprocMetastoreClient.parse_network_path)
    service_path = staticmethod(DataprocMetastoreClient.service_path)
    parse_service_path = staticmethod(DataprocMetastoreClient.parse_service_path)
    common_billing_account_path = staticmethod(
        DataprocMetastoreClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        DataprocMetastoreClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(DataprocMetastoreClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        DataprocMetastoreClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        DataprocMetastoreClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        DataprocMetastoreClient.parse_common_organization_path
    )
    common_project_path = staticmethod(DataprocMetastoreClient.common_project_path)
    parse_common_project_path = staticmethod(
        DataprocMetastoreClient.parse_common_project_path
    )
    common_location_path = staticmethod(DataprocMetastoreClient.common_location_path)
    parse_common_location_path = staticmethod(
        DataprocMetastoreClient.parse_common_location_path
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
            DataprocMetastoreAsyncClient: The constructed client.
        """
        return DataprocMetastoreClient.from_service_account_info.__func__(DataprocMetastoreAsyncClient, info, *args, **kwargs)  # type: ignore

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
            DataprocMetastoreAsyncClient: The constructed client.
        """
        return DataprocMetastoreClient.from_service_account_file.__func__(DataprocMetastoreAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DataprocMetastoreTransport:
        """Returns the transport used by the client instance.

        Returns:
            DataprocMetastoreTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(DataprocMetastoreClient).get_transport_class, type(DataprocMetastoreClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, DataprocMetastoreTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the dataproc metastore client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.DataprocMetastoreTransport]): The
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
        self._client = DataprocMetastoreClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_services(
        self,
        request: metastore.ListServicesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServicesAsyncPager:
        r"""Lists services in a project and location.

        Args:
            request (:class:`google.cloud.metastore_v1.types.ListServicesRequest`):
                The request object. Request message for
                [DataprocMetastore.ListServices][google.cloud.metastore.v1.DataprocMetastore.ListServices].
            parent (:class:`str`):
                Required. The relative resource name of the location of
                metastore services to list, in the following form:

                ``projects/{project_number}/locations/{location_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.metastore_v1.services.dataproc_metastore.pagers.ListServicesAsyncPager:
                Response message for
                [DataprocMetastore.ListServices][google.cloud.metastore.v1.DataprocMetastore.ListServices].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metastore.ListServicesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_services,
            default_timeout=None,
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
        response = pagers.ListServicesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_service(
        self,
        request: metastore.GetServiceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metastore.Service:
        r"""Gets the details of a single service.

        Args:
            request (:class:`google.cloud.metastore_v1.types.GetServiceRequest`):
                The request object. Request message for
                [DataprocMetastore.GetService][google.cloud.metastore.v1.DataprocMetastore.GetService].
            name (:class:`str`):
                Required. The relative resource name of the metastore
                service to retrieve, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.metastore_v1.types.Service:
                A managed metastore service that
                serves metadata queries.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metastore.GetServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_service,
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

        # Done; return the response.
        return response

    async def create_service(
        self,
        request: metastore.CreateServiceRequest = None,
        *,
        parent: str = None,
        service: metastore.Service = None,
        service_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a metastore service in a project and
        location.

        Args:
            request (:class:`google.cloud.metastore_v1.types.CreateServiceRequest`):
                The request object. Request message for
                [DataprocMetastore.CreateService][google.cloud.metastore.v1.DataprocMetastore.CreateService].
            parent (:class:`str`):
                Required. The relative resource name of the location in
                which to create a metastore service, in the following
                form:

                ``projects/{project_number}/locations/{location_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service (:class:`google.cloud.metastore_v1.types.Service`):
                Required. The Metastore service to create. The ``name``
                field is ignored. The ID of the created metastore
                service must be provided in the request's ``service_id``
                field.

                This corresponds to the ``service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service_id (:class:`str`):
                Required. The ID of the metastore
                service, which is used as the final
                component of the metastore service's
                name.
                This value must be between 2 and 63
                characters long inclusive, begin with a
                letter, end with a letter or number, and
                consist of alpha-numeric ASCII
                characters or hyphens.

                This corresponds to the ``service_id`` field
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
                :class:`google.cloud.metastore_v1.types.Service` A
                managed metastore service that serves metadata queries.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, service, service_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metastore.CreateServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if service is not None:
            request.service = service
        if service_id is not None:
            request.service_id = service_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_service,
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
            metastore.Service,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_service(
        self,
        request: metastore.UpdateServiceRequest = None,
        *,
        service: metastore.Service = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single service.

        Args:
            request (:class:`google.cloud.metastore_v1.types.UpdateServiceRequest`):
                The request object. Request message for
                [DataprocMetastore.UpdateService][google.cloud.metastore.v1.DataprocMetastore.UpdateService].
            service (:class:`google.cloud.metastore_v1.types.Service`):
                Required. The metastore service to update. The server
                only merges fields in the service if they are specified
                in ``update_mask``.

                The metastore service's ``name`` field is used to
                identify the metastore service to be updated.

                This corresponds to the ``service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. A field mask used to specify the fields to be
                overwritten in the metastore service resource by the
                update. Fields specified in the ``update_mask`` are
                relative to the resource (not to the full request). A
                field is overwritten if it is in the mask.

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
                :class:`google.cloud.metastore_v1.types.Service` A
                managed metastore service that serves metadata queries.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metastore.UpdateServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service is not None:
            request.service = service
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_service,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("service.name", request.service.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            metastore.Service,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_service(
        self,
        request: metastore.DeleteServiceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single service.

        Args:
            request (:class:`google.cloud.metastore_v1.types.DeleteServiceRequest`):
                The request object. Request message for
                [DataprocMetastore.DeleteService][google.cloud.metastore.v1.DataprocMetastore.DeleteService].
            name (:class:`str`):
                Required. The relative resource name of the metastore
                service to delete, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}``.

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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metastore.DeleteServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_service,
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
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_metadata_imports(
        self,
        request: metastore.ListMetadataImportsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMetadataImportsAsyncPager:
        r"""Lists imports in a service.

        Args:
            request (:class:`google.cloud.metastore_v1.types.ListMetadataImportsRequest`):
                The request object. Request message for
                [DataprocMetastore.ListMetadataImports][google.cloud.metastore.v1.DataprocMetastore.ListMetadataImports].
            parent (:class:`str`):
                Required. The relative resource name of the service
                whose metadata imports to list, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}/metadataImports``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.metastore_v1.services.dataproc_metastore.pagers.ListMetadataImportsAsyncPager:
                Response message for
                [DataprocMetastore.ListMetadataImports][google.cloud.metastore.v1.DataprocMetastore.ListMetadataImports].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metastore.ListMetadataImportsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_metadata_imports,
            default_timeout=None,
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
        response = pagers.ListMetadataImportsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_metadata_import(
        self,
        request: metastore.GetMetadataImportRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> metastore.MetadataImport:
        r"""Gets details of a single import.

        Args:
            request (:class:`google.cloud.metastore_v1.types.GetMetadataImportRequest`):
                The request object. Request message for
                [DataprocMetastore.GetMetadataImport][google.cloud.metastore.v1.DataprocMetastore.GetMetadataImport].
            name (:class:`str`):
                Required. The relative resource name of the metadata
                import to retrieve, in the following form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}/metadataImports/{import_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.metastore_v1.types.MetadataImport:
                A metastore resource that imports
                metadata.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metastore.GetMetadataImportRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_metadata_import,
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

        # Done; return the response.
        return response

    async def create_metadata_import(
        self,
        request: metastore.CreateMetadataImportRequest = None,
        *,
        parent: str = None,
        metadata_import: metastore.MetadataImport = None,
        metadata_import_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new MetadataImport in a given project and
        location.

        Args:
            request (:class:`google.cloud.metastore_v1.types.CreateMetadataImportRequest`):
                The request object. Request message for
                [DataprocMetastore.CreateMetadataImport][google.cloud.metastore.v1.DataprocMetastore.CreateMetadataImport].
            parent (:class:`str`):
                Required. The relative resource name of the service in
                which to create a metastore import, in the following
                form:

                ``projects/{project_number}/locations/{location_id}/services/{service_id}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metadata_import (:class:`google.cloud.metastore_v1.types.MetadataImport`):
                Required. The metadata import to create. The ``name``
                field is ignored. The ID of the created metadata import
                must be provided in the request's ``metadata_import_id``
                field.

                This corresponds to the ``metadata_import`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            metadata_import_id (:class:`str`):
                Required. The ID of the metadata
                import, which is used as the final
                component of the metadata import's name.
                This value must be between 1 and 64
                characters long, begin with a letter,
                end with a letter or number, and consist
                of alpha-numeric ASCII characters or
                hyphens.

                This corresponds to the ``metadata_import_id`` field
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
                :class:`google.cloud.metastore_v1.types.MetadataImport`
                A metastore resource that imports metadata.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, metadata_import, metadata_import_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metastore.CreateMetadataImportRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if metadata_import is not None:
            request.metadata_import = metadata_import
        if metadata_import_id is not None:
            request.metadata_import_id = metadata_import_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_metadata_import,
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
            metastore.MetadataImport,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_metadata_import(
        self,
        request: metastore.UpdateMetadataImportRequest = None,
        *,
        metadata_import: metastore.MetadataImport = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates a single import.
        Only the description field of MetadataImport is
        supported to be updated.

        Args:
            request (:class:`google.cloud.metastore_v1.types.UpdateMetadataImportRequest`):
                The request object. Request message for
                [DataprocMetastore.UpdateMetadataImport][google.cloud.metastore.v1.DataprocMetastore.UpdateMetadataImport].
            metadata_import (:class:`google.cloud.metastore_v1.types.MetadataImport`):
                Required. The metadata import to update. The server only
                merges fields in the import if they are specified in
                ``update_mask``.

                The metadata import's ``name`` field is used to identify
                the metastore import to be updated.

                This corresponds to the ``metadata_import`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. A field mask used to specify the fields to be
                overwritten in the metadata import resource by the
                update. Fields specified in the ``update_mask`` are
                relative to the resource (not to the full request). A
                field is overwritten if it is in the mask.

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
                :class:`google.cloud.metastore_v1.types.MetadataImport`
                A metastore resource that imports metadata.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([metadata_import, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = metastore.UpdateMetadataImportRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if metadata_import is not None:
            request.metadata_import = metadata_import
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_metadata_import,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("metadata_import.name", request.metadata_import.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            metastore.MetadataImport,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def export_metadata(
        self,
        request: metastore.ExportMetadataRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Exports metadata from a service.

        Args:
            request (:class:`google.cloud.metastore_v1.types.ExportMetadataRequest`):
                The request object. Request message for
                [DataprocMetastore.ExportMetadata][google.cloud.metastore.v1.DataprocMetastore.ExportMetadata].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.metastore_v1.types.MetadataExport`
                The details of a metadata export operation.

        """
        # Create or coerce a protobuf request object.
        request = metastore.ExportMetadataRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.export_metadata,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("service", request.service),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            metastore.MetadataExport,
            metadata_type=metastore.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-metastore",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("DataprocMetastoreAsyncClient",)
