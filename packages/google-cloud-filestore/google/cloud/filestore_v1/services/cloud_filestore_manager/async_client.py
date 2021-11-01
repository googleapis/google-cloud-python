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

from google.api_core.client_options import ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

OptionalRetry = Union[retries.Retry, object]

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.common.types import operation_metadata as operation_metadata_pb2  # type: ignore
from google.cloud.filestore_v1.services.cloud_filestore_manager import pagers
from google.cloud.filestore_v1.types import cloud_filestore_service
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from .transports.base import CloudFilestoreManagerTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CloudFilestoreManagerGrpcAsyncIOTransport
from .client import CloudFilestoreManagerClient


class CloudFilestoreManagerAsyncClient:
    """Configures and manages Cloud Filestore resources.

    Cloud Filestore Manager v1.

    The ``file.googleapis.com`` service implements the Cloud Filestore
    API and defines the following resource model for managing instances:

    -  The service works with a collection of cloud projects, named:
       ``/projects/*``
    -  Each project has a collection of available locations, named:
       ``/locations/*``
    -  Each location has a collection of instances and backups, named:
       ``/instances/*`` and ``/backups/*`` respectively.
    -  As such, Cloud Filestore instances are resources of the form:
       ``/projects/{project_number}/locations/{location_id}/instances/{instance_id}``
       and backups are resources of the form:
       ``/projects/{project_number}/locations/{location_id}/backup/{backup_id}``

    Note that location_id must be a GCP ``zone`` for instances and but
    to a GCP ``region`` for backups; for example:

    -  ``projects/12345/locations/us-central1-c/instances/my-filestore``
    -  ``projects/12345/locations/us-central1/backups/my-backup``
    """

    _client: CloudFilestoreManagerClient

    DEFAULT_ENDPOINT = CloudFilestoreManagerClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CloudFilestoreManagerClient.DEFAULT_MTLS_ENDPOINT

    backup_path = staticmethod(CloudFilestoreManagerClient.backup_path)
    parse_backup_path = staticmethod(CloudFilestoreManagerClient.parse_backup_path)
    instance_path = staticmethod(CloudFilestoreManagerClient.instance_path)
    parse_instance_path = staticmethod(CloudFilestoreManagerClient.parse_instance_path)
    common_billing_account_path = staticmethod(
        CloudFilestoreManagerClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CloudFilestoreManagerClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CloudFilestoreManagerClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        CloudFilestoreManagerClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        CloudFilestoreManagerClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        CloudFilestoreManagerClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CloudFilestoreManagerClient.common_project_path)
    parse_common_project_path = staticmethod(
        CloudFilestoreManagerClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        CloudFilestoreManagerClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        CloudFilestoreManagerClient.parse_common_location_path
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
            CloudFilestoreManagerAsyncClient: The constructed client.
        """
        return CloudFilestoreManagerClient.from_service_account_info.__func__(CloudFilestoreManagerAsyncClient, info, *args, **kwargs)  # type: ignore

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
            CloudFilestoreManagerAsyncClient: The constructed client.
        """
        return CloudFilestoreManagerClient.from_service_account_file.__func__(CloudFilestoreManagerAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CloudFilestoreManagerTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudFilestoreManagerTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CloudFilestoreManagerClient).get_transport_class,
        type(CloudFilestoreManagerClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CloudFilestoreManagerTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud filestore manager client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CloudFilestoreManagerTransport]): The
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
        self._client = CloudFilestoreManagerClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_instances(
        self,
        request: Union[cloud_filestore_service.ListInstancesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInstancesAsyncPager:
        r"""Lists all instances in a project for either a
        specified location or for all locations.

        Args:
            request (Union[google.cloud.filestore_v1.types.ListInstancesRequest, dict]):
                The request object. ListInstancesRequest lists
                instances.
            parent (:class:`str`):
                Required. The project and location for which to retrieve
                instance information, in the format
                ``projects/{project_id}/locations/{location}``. In Cloud
                Filestore, locations map to GCP zones, for example
                **us-west1-b**. To retrieve instance information for all
                locations, use "-" for the ``{location}`` value.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.filestore_v1.services.cloud_filestore_manager.pagers.ListInstancesAsyncPager:
                ListInstancesResponse is the result
                of ListInstancesRequest.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = cloud_filestore_service.ListInstancesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_instances,
            default_retry=retries.Retry(
                initial=0.25,
                maximum=32.0,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListInstancesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_instance(
        self,
        request: Union[cloud_filestore_service.GetInstanceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_filestore_service.Instance:
        r"""Gets the details of a specific instance.

        Args:
            request (Union[google.cloud.filestore_v1.types.GetInstanceRequest, dict]):
                The request object. GetInstanceRequest gets the state of
                an instance.
            name (:class:`str`):
                Required. The instance resource name, in the format
                ``projects/{project_id}/locations/{location}/instances/{instance_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.filestore_v1.types.Instance:
                A Cloud Filestore instance.
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

        request = cloud_filestore_service.GetInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_instance,
            default_retry=retries.Retry(
                initial=0.25,
                maximum=32.0,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_instance(
        self,
        request: Union[cloud_filestore_service.CreateInstanceRequest, dict] = None,
        *,
        parent: str = None,
        instance: cloud_filestore_service.Instance = None,
        instance_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates an instance.
        When creating from a backup, the capacity of the new
        instance needs to be equal to or larger than the
        capacity of the backup (and also equal to or larger than
        the minimum capacity of the tier).

        Args:
            request (Union[google.cloud.filestore_v1.types.CreateInstanceRequest, dict]):
                The request object. CreateInstanceRequest creates an
                instance.
            parent (:class:`str`):
                Required. The instance's project and location, in the
                format ``projects/{project_id}/locations/{location}``.
                In Cloud Filestore, locations map to GCP zones, for
                example **us-west1-b**.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (:class:`google.cloud.filestore_v1.types.Instance`):
                Required. An [instance
                resource][google.cloud.filestore.v1.Instance]

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_id (:class:`str`):
                Required. The name of the instance to
                create. The name must be unique for the
                specified project and location.

                This corresponds to the ``instance_id`` field
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
                :class:`google.cloud.filestore_v1.types.Instance` A
                Cloud Filestore instance.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, instance, instance_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_filestore_service.CreateInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if instance is not None:
            request.instance = instance
        if instance_id is not None:
            request.instance_id = instance_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_instance,
            default_timeout=60000.0,
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
            cloud_filestore_service.Instance,
            metadata_type=operation_metadata_pb2.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_instance(
        self,
        request: Union[cloud_filestore_service.UpdateInstanceRequest, dict] = None,
        *,
        instance: cloud_filestore_service.Instance = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the settings of a specific instance.

        Args:
            request (Union[google.cloud.filestore_v1.types.UpdateInstanceRequest, dict]):
                The request object. UpdateInstanceRequest updates the
                settings of an instance.
            instance (:class:`google.cloud.filestore_v1.types.Instance`):
                Only fields specified in update_mask are updated.
                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Mask of fields to update. At least one path must be
                supplied in this field. The elements of the repeated
                paths field may only include these fields:

                -  "description"
                -  "file_shares"
                -  "labels"

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
                :class:`google.cloud.filestore_v1.types.Instance` A
                Cloud Filestore instance.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([instance, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_filestore_service.UpdateInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if instance is not None:
            request.instance = instance
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_instance,
            default_timeout=14400.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("instance.name", request.instance.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_filestore_service.Instance,
            metadata_type=operation_metadata_pb2.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def restore_instance(
        self,
        request: Union[cloud_filestore_service.RestoreInstanceRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Restores an existing instance's file share from a
        backup.
        The capacity of the instance needs to be equal to or
        larger than the capacity of the backup (and also equal
        to or larger than the minimum capacity of the tier).

        Args:
            request (Union[google.cloud.filestore_v1.types.RestoreInstanceRequest, dict]):
                The request object. RestoreInstanceRequest restores an
                existing instances's file share from a backup.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.filestore_v1.types.Instance` A
                Cloud Filestore instance.

        """
        # Create or coerce a protobuf request object.
        request = cloud_filestore_service.RestoreInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.restore_instance,
            default_timeout=60000.0,
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
            cloud_filestore_service.Instance,
            metadata_type=operation_metadata_pb2.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_instance(
        self,
        request: Union[cloud_filestore_service.DeleteInstanceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes an instance.

        Args:
            request (Union[google.cloud.filestore_v1.types.DeleteInstanceRequest, dict]):
                The request object. DeleteInstanceRequest deletes an
                instance.
            name (:class:`str`):
                Required. The instance resource name, in the format
                ``projects/{project_id}/locations/{location}/instances/{instance_id}``

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

        request = cloud_filestore_service.DeleteInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_instance,
            default_timeout=600.0,
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
            metadata_type=operation_metadata_pb2.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_backups(
        self,
        request: Union[cloud_filestore_service.ListBackupsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBackupsAsyncPager:
        r"""Lists all backups in a project for either a specified
        location or for all locations.

        Args:
            request (Union[google.cloud.filestore_v1.types.ListBackupsRequest, dict]):
                The request object. ListBackupsRequest lists backups.
            parent (:class:`str`):
                Required. The project and location for which to retrieve
                backup information, in the format
                ``projects/{project_number}/locations/{location}``. In
                Cloud Filestore, backup locations map to GCP regions,
                for example **us-west1**. To retrieve backup information
                for all locations, use "-" for the ``{location}`` value.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.filestore_v1.services.cloud_filestore_manager.pagers.ListBackupsAsyncPager:
                ListBackupsResponse is the result of
                ListBackupsRequest.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

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

        request = cloud_filestore_service.ListBackupsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_backups,
            default_retry=retries.Retry(
                initial=0.25,
                maximum=32.0,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListBackupsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_backup(
        self,
        request: Union[cloud_filestore_service.GetBackupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_filestore_service.Backup:
        r"""Gets the details of a specific backup.

        Args:
            request (Union[google.cloud.filestore_v1.types.GetBackupRequest, dict]):
                The request object. GetBackupRequest gets the state of a
                backup.
            name (:class:`str`):
                Required. The backup resource name, in the format
                ``projects/{project_number}/locations/{location}/backups/{backup_id}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.filestore_v1.types.Backup:
                A Cloud Filestore backup.
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

        request = cloud_filestore_service.GetBackupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_backup,
            default_retry=retries.Retry(
                initial=0.25,
                maximum=32.0,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_backup(
        self,
        request: Union[cloud_filestore_service.CreateBackupRequest, dict] = None,
        *,
        parent: str = None,
        backup: cloud_filestore_service.Backup = None,
        backup_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a backup.

        Args:
            request (Union[google.cloud.filestore_v1.types.CreateBackupRequest, dict]):
                The request object. CreateBackupRequest creates a
                backup.
            parent (:class:`str`):
                Required. The backup's project and location, in the
                format
                ``projects/{project_number}/locations/{location}``. In
                Cloud Filestore, backup locations map to GCP regions,
                for example **us-west1**.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup (:class:`google.cloud.filestore_v1.types.Backup`):
                Required. A [backup
                resource][google.cloud.filestore.v1.Backup]

                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_id (:class:`str`):
                Required. The ID to use for the backup. The ID must be
                unique within the specified project and location.

                This value must start with a lowercase letter followed
                by up to 62 lowercase letters, numbers, or hyphens, and
                cannot end with a hyphen. Values that do not match this
                pattern will trigger an INVALID_ARGUMENT error.

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

                The result type for the operation will be
                :class:`google.cloud.filestore_v1.types.Backup` A Cloud
                Filestore backup.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, backup, backup_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_filestore_service.CreateBackupRequest(request)

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
            default_timeout=60000.0,
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
            cloud_filestore_service.Backup,
            metadata_type=operation_metadata_pb2.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_backup(
        self,
        request: Union[cloud_filestore_service.DeleteBackupRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a backup.

        Args:
            request (Union[google.cloud.filestore_v1.types.DeleteBackupRequest, dict]):
                The request object. DeleteBackupRequest deletes a
                backup.
            name (:class:`str`):
                Required. The backup resource name, in the format
                ``projects/{project_number}/locations/{location}/backups/{backup_id}``

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

        request = cloud_filestore_service.DeleteBackupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_backup,
            default_timeout=600.0,
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
            metadata_type=operation_metadata_pb2.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_backup(
        self,
        request: Union[cloud_filestore_service.UpdateBackupRequest, dict] = None,
        *,
        backup: cloud_filestore_service.Backup = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the settings of a specific backup.

        Args:
            request (Union[google.cloud.filestore_v1.types.UpdateBackupRequest, dict]):
                The request object. UpdateBackupRequest updates
                description and/or labels for a backup.
            backup (:class:`google.cloud.filestore_v1.types.Backup`):
                Required. A [backup
                resource][google.cloud.filestore.v1.Backup]

                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Mask of fields to update.
                At least one path must be supplied in
                this field.

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
                :class:`google.cloud.filestore_v1.types.Backup` A Cloud
                Filestore backup.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([backup, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_filestore_service.UpdateBackupRequest(request)

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
            default_timeout=600.0,
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
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_filestore_service.Backup,
            metadata_type=operation_metadata_pb2.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-filestore",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudFilestoreManagerAsyncClient",)
