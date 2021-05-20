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
from google.cloud.memcache_v1beta2.services.cloud_memcache import pagers
from google.cloud.memcache_v1beta2.types import cloud_memcache
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import CloudMemcacheTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CloudMemcacheGrpcAsyncIOTransport
from .client import CloudMemcacheClient


class CloudMemcacheAsyncClient:
    """Configures and manages Cloud Memorystore for Memcached instances.

    The ``memcache.googleapis.com`` service implements the Google Cloud
    Memorystore for Memcached API and defines the following resource
    model for managing Memorystore Memcached (also called Memcached
    below) instances:

    -  The service works with a collection of cloud projects, named:
       ``/projects/*``
    -  Each project has a collection of available locations, named:
       ``/locations/*``
    -  Each location has a collection of Memcached instances, named:
       ``/instances/*``
    -  As such, Memcached instances are resources of the form:
       ``/projects/{project_id}/locations/{location_id}/instances/{instance_id}``

    Note that location_id must be a GCP ``region``; for example:

    -  ``projects/my-memcached-project/locations/us-central1/instances/my-memcached``
    """

    _client: CloudMemcacheClient

    DEFAULT_ENDPOINT = CloudMemcacheClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CloudMemcacheClient.DEFAULT_MTLS_ENDPOINT

    instance_path = staticmethod(CloudMemcacheClient.instance_path)
    parse_instance_path = staticmethod(CloudMemcacheClient.parse_instance_path)
    common_billing_account_path = staticmethod(
        CloudMemcacheClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CloudMemcacheClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CloudMemcacheClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        CloudMemcacheClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        CloudMemcacheClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        CloudMemcacheClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CloudMemcacheClient.common_project_path)
    parse_common_project_path = staticmethod(
        CloudMemcacheClient.parse_common_project_path
    )
    common_location_path = staticmethod(CloudMemcacheClient.common_location_path)
    parse_common_location_path = staticmethod(
        CloudMemcacheClient.parse_common_location_path
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
            CloudMemcacheAsyncClient: The constructed client.
        """
        return CloudMemcacheClient.from_service_account_info.__func__(CloudMemcacheAsyncClient, info, *args, **kwargs)  # type: ignore

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
            CloudMemcacheAsyncClient: The constructed client.
        """
        return CloudMemcacheClient.from_service_account_file.__func__(CloudMemcacheAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> CloudMemcacheTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudMemcacheTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CloudMemcacheClient).get_transport_class, type(CloudMemcacheClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CloudMemcacheTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud memcache client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CloudMemcacheTransport]): The
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
        self._client = CloudMemcacheClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_instances(
        self,
        request: cloud_memcache.ListInstancesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInstancesAsyncPager:
        r"""Lists Instances in a given location.

        Args:
            request (:class:`google.cloud.memcache_v1beta2.types.ListInstancesRequest`):
                The request object. Request for
                [ListInstances][google.cloud.memcache.v1beta2.CloudMemcache.ListInstances].
            parent (:class:`str`):
                Required. The resource name of the instance location
                using the form:
                ``projects/{project_id}/locations/{location_id}`` where
                ``location_id`` refers to a GCP region

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.memcache_v1beta2.services.cloud_memcache.pagers.ListInstancesAsyncPager:
                Response for
                [ListInstances][google.cloud.memcache.v1beta2.CloudMemcache.ListInstances].

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

        request = cloud_memcache.ListInstancesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_instances,
            default_timeout=1200.0,
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
        request: cloud_memcache.GetInstanceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_memcache.Instance:
        r"""Gets details of a single Instance.

        Args:
            request (:class:`google.cloud.memcache_v1beta2.types.GetInstanceRequest`):
                The request object. Request for
                [GetInstance][google.cloud.memcache.v1beta2.CloudMemcache.GetInstance].
            name (:class:`str`):
                Required. Memcached instance resource name in the
                format:
                ``projects/{project_id}/locations/{location_id}/instances/{instance_id}``
                where ``location_id`` refers to a GCP region

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.memcache_v1beta2.types.Instance:
                A Memorystore for Memcached instance
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

        request = cloud_memcache.GetInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_instance,
            default_timeout=1200.0,
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
        request: cloud_memcache.CreateInstanceRequest = None,
        *,
        parent: str = None,
        instance_id: str = None,
        resource: cloud_memcache.Instance = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Instance in a given location.

        Args:
            request (:class:`google.cloud.memcache_v1beta2.types.CreateInstanceRequest`):
                The request object. Request for
                [CreateInstance][google.cloud.memcache.v1beta2.CloudMemcache.CreateInstance].
            parent (:class:`str`):
                Required. The resource name of the instance location
                using the form:
                ``projects/{project_id}/locations/{location_id}`` where
                ``location_id`` refers to a GCP region

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_id (:class:`str`):
                Required. The logical name of the Memcached instance in
                the user project with the following restrictions:

                -  Must contain only lowercase letters, numbers, and
                   hyphens.
                -  Must start with a letter.
                -  Must be between 1-40 characters.
                -  Must end with a number or a letter.
                -  Must be unique within the user project / location.

                If any of the above are not met, the API raises an
                invalid argument error.

                This corresponds to the ``instance_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (:class:`google.cloud.memcache_v1beta2.types.Instance`):
                Required. A Memcached [Instance] resource
                This corresponds to the ``resource`` field
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
                :class:`google.cloud.memcache_v1beta2.types.Instance` A
                Memorystore for Memcached instance

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, instance_id, resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_memcache.CreateInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if instance_id is not None:
            request.instance_id = instance_id
        if resource is not None:
            request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_instance,
            default_timeout=1200.0,
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
            cloud_memcache.Instance,
            metadata_type=cloud_memcache.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_instance(
        self,
        request: cloud_memcache.UpdateInstanceRequest = None,
        *,
        update_mask: field_mask_pb2.FieldMask = None,
        resource: cloud_memcache.Instance = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates an existing Instance in a given project and
        location.

        Args:
            request (:class:`google.cloud.memcache_v1beta2.types.UpdateInstanceRequest`):
                The request object. Request for
                [UpdateInstance][google.cloud.memcache.v1beta2.CloudMemcache.UpdateInstance].
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Mask of fields to update.

                -  ``displayName``

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (:class:`google.cloud.memcache_v1beta2.types.Instance`):
                Required. A Memcached [Instance] resource. Only fields
                specified in update_mask are updated.

                This corresponds to the ``resource`` field
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
                :class:`google.cloud.memcache_v1beta2.types.Instance` A
                Memorystore for Memcached instance

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([update_mask, resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_memcache.UpdateInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if update_mask is not None:
            request.update_mask = update_mask
        if resource is not None:
            request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_instance,
            default_timeout=1200.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("resource.name", request.resource.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_memcache.Instance,
            metadata_type=cloud_memcache.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_parameters(
        self,
        request: cloud_memcache.UpdateParametersRequest = None,
        *,
        name: str = None,
        update_mask: field_mask_pb2.FieldMask = None,
        parameters: cloud_memcache.MemcacheParameters = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the defined Memcached parameters for an existing
        instance. This method only stages the parameters, it must be
        followed by ``ApplyParameters`` to apply the parameters to nodes
        of the Memcached instance.

        Args:
            request (:class:`google.cloud.memcache_v1beta2.types.UpdateParametersRequest`):
                The request object. Request for
                [UpdateParameters][google.cloud.memcache.v1beta2.CloudMemcache.UpdateParameters].
            name (:class:`str`):
                Required. Resource name of the
                Memcached instance for which the
                parameters should be updated.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Mask of fields to update.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parameters (:class:`google.cloud.memcache_v1beta2.types.MemcacheParameters`):
                The parameters to apply to the
                instance.

                This corresponds to the ``parameters`` field
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
                :class:`google.cloud.memcache_v1beta2.types.Instance` A
                Memorystore for Memcached instance

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, update_mask, parameters])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_memcache.UpdateParametersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if update_mask is not None:
            request.update_mask = update_mask
        if parameters is not None:
            request.parameters = parameters

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_parameters,
            default_timeout=1200.0,
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
            cloud_memcache.Instance,
            metadata_type=cloud_memcache.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_instance(
        self,
        request: cloud_memcache.DeleteInstanceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Instance.

        Args:
            request (:class:`google.cloud.memcache_v1beta2.types.DeleteInstanceRequest`):
                The request object. Request for
                [DeleteInstance][google.cloud.memcache.v1beta2.CloudMemcache.DeleteInstance].
            name (:class:`str`):
                Required. Memcached instance resource name in the
                format:
                ``projects/{project_id}/locations/{location_id}/instances/{instance_id}``
                where ``location_id`` refers to a GCP region

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

        request = cloud_memcache.DeleteInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_instance,
            default_timeout=1200.0,
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
            metadata_type=cloud_memcache.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def apply_parameters(
        self,
        request: cloud_memcache.ApplyParametersRequest = None,
        *,
        name: str = None,
        node_ids: Sequence[str] = None,
        apply_all: bool = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""``ApplyParameters`` restarts the set of specified nodes in order
        to update them to the current set of parameters for the
        Memcached Instance.

        Args:
            request (:class:`google.cloud.memcache_v1beta2.types.ApplyParametersRequest`):
                The request object. Request for
                [ApplyParameters][google.cloud.memcache.v1beta2.CloudMemcache.ApplyParameters].
            name (:class:`str`):
                Required. Resource name of the
                Memcached instance for which parameter
                group updates should be applied.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_ids (:class:`Sequence[str]`):
                Nodes to which the instance-level
                parameter group is applied.

                This corresponds to the ``node_ids`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            apply_all (:class:`bool`):
                Whether to apply instance-level parameter group to all
                nodes. If set to true, users are restricted from
                specifying individual nodes, and ``ApplyParameters``
                updates all nodes within the instance.

                This corresponds to the ``apply_all`` field
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
                :class:`google.cloud.memcache_v1beta2.types.Instance` A
                Memorystore for Memcached instance

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, node_ids, apply_all])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_memcache.ApplyParametersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if apply_all is not None:
            request.apply_all = apply_all
        if node_ids:
            request.node_ids.extend(node_ids)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.apply_parameters,
            default_timeout=1200.0,
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
            cloud_memcache.Instance,
            metadata_type=cloud_memcache.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def apply_software_update(
        self,
        request: cloud_memcache.ApplySoftwareUpdateRequest = None,
        *,
        instance: str = None,
        node_ids: Sequence[str] = None,
        apply_all: bool = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates software on the selected nodes of the
        Instance.

        Args:
            request (:class:`google.cloud.memcache_v1beta2.types.ApplySoftwareUpdateRequest`):
                The request object. Request for
                [ApplySoftwareUpdate][google.cloud.memcache.v1beta2.CloudMemcache.ApplySoftwareUpdate].
            instance (:class:`str`):
                Required. Resource name of the
                Memcached instance for which software
                update should be applied.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_ids (:class:`Sequence[str]`):
                Nodes to which we should apply the
                update to. Note all the selected nodes
                are updated in parallel.

                This corresponds to the ``node_ids`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            apply_all (:class:`bool`):
                Whether to apply the update to all
                nodes. If set to true, will explicitly
                restrict users from specifying any
                nodes, and apply software update to all
                nodes (where applicable) within the
                instance.

                This corresponds to the ``apply_all`` field
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
                :class:`google.cloud.memcache_v1beta2.types.Instance` A
                Memorystore for Memcached instance

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([instance, node_ids, apply_all])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_memcache.ApplySoftwareUpdateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if instance is not None:
            request.instance = instance
        if apply_all is not None:
            request.apply_all = apply_all
        if node_ids:
            request.node_ids.extend(node_ids)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.apply_software_update,
            default_timeout=1200.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("instance", request.instance),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_memcache.Instance,
            metadata_type=cloud_memcache.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-memcache",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudMemcacheAsyncClient",)
