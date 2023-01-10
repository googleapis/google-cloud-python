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

from google.cloud.dataproc_v1 import gapic_version as package_version

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
from google.cloud.dataproc_v1.types import clusters
from google.cloud.dataproc_v1.types import node_groups
from google.cloud.dataproc_v1.types import operations
from .transports.base import NodeGroupControllerTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import NodeGroupControllerGrpcAsyncIOTransport
from .client import NodeGroupControllerClient


class NodeGroupControllerAsyncClient:
    """The ``NodeGroupControllerService`` provides methods to manage node
    groups of Compute Engine managed instances.
    """

    _client: NodeGroupControllerClient

    DEFAULT_ENDPOINT = NodeGroupControllerClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = NodeGroupControllerClient.DEFAULT_MTLS_ENDPOINT

    node_group_path = staticmethod(NodeGroupControllerClient.node_group_path)
    parse_node_group_path = staticmethod(
        NodeGroupControllerClient.parse_node_group_path
    )
    common_billing_account_path = staticmethod(
        NodeGroupControllerClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        NodeGroupControllerClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(NodeGroupControllerClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        NodeGroupControllerClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        NodeGroupControllerClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        NodeGroupControllerClient.parse_common_organization_path
    )
    common_project_path = staticmethod(NodeGroupControllerClient.common_project_path)
    parse_common_project_path = staticmethod(
        NodeGroupControllerClient.parse_common_project_path
    )
    common_location_path = staticmethod(NodeGroupControllerClient.common_location_path)
    parse_common_location_path = staticmethod(
        NodeGroupControllerClient.parse_common_location_path
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
            NodeGroupControllerAsyncClient: The constructed client.
        """
        return NodeGroupControllerClient.from_service_account_info.__func__(NodeGroupControllerAsyncClient, info, *args, **kwargs)  # type: ignore

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
            NodeGroupControllerAsyncClient: The constructed client.
        """
        return NodeGroupControllerClient.from_service_account_file.__func__(NodeGroupControllerAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return NodeGroupControllerClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> NodeGroupControllerTransport:
        """Returns the transport used by the client instance.

        Returns:
            NodeGroupControllerTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(NodeGroupControllerClient).get_transport_class,
        type(NodeGroupControllerClient),
    )

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, NodeGroupControllerTransport] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the node group controller client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.NodeGroupControllerTransport]): The
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
        self._client = NodeGroupControllerClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_node_group(
        self,
        request: Optional[Union[node_groups.CreateNodeGroupRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        node_group: Optional[clusters.NodeGroup] = None,
        node_group_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a node group in a cluster. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] is
        `NodeGroupOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#nodegroupoperationmetadata>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            async def sample_create_node_group():
                # Create a client
                client = dataproc_v1.NodeGroupControllerAsyncClient()

                # Initialize request argument(s)
                node_group = dataproc_v1.NodeGroup()
                node_group.roles = ['DRIVER']

                request = dataproc_v1.CreateNodeGroupRequest(
                    parent="parent_value",
                    node_group=node_group,
                )

                # Make the request
                operation = client.create_node_group(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.dataproc_v1.types.CreateNodeGroupRequest, dict]]):
                The request object. A request to create a node group.
            parent (:class:`str`):
                Required. The parent resource where this node group will
                be created. Format:
                ``projects/{project}/regions/{region}/clusters/{cluster}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_group (:class:`google.cloud.dataproc_v1.types.NodeGroup`):
                Required. The node group to create.
                This corresponds to the ``node_group`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            node_group_id (:class:`str`):
                Optional. An optional node group ID. Generated if not
                specified.

                The ID must contain only letters (a-z, A-Z), numbers
                (0-9), underscores (_), and hyphens (-). Cannot begin or
                end with underscore or hyphen. Must consist of from 3 to
                33 characters.

                This corresponds to the ``node_group_id`` field
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

                The result type for the operation will be :class:`google.cloud.dataproc_v1.types.NodeGroup` Dataproc Node Group.
                   **The Dataproc NodeGroup resource is not related to
                   the Dataproc
                   [NodeGroupAffinity][google.cloud.dataproc.v1.NodeGroupAffinity]
                   resource.**

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, node_group, node_group_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = node_groups.CreateNodeGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if node_group is not None:
            request.node_group = node_group
        if node_group_id is not None:
            request.node_group_id = node_group_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_node_group,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            clusters.NodeGroup,
            metadata_type=operations.NodeGroupOperationMetadata,
        )

        # Done; return the response.
        return response

    async def resize_node_group(
        self,
        request: Optional[Union[node_groups.ResizeNodeGroupRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        size: Optional[int] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Resizes a node group in a cluster. The returned
        [Operation.metadata][google.longrunning.Operation.metadata] is
        `NodeGroupOperationMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#nodegroupoperationmetadata>`__.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            async def sample_resize_node_group():
                # Create a client
                client = dataproc_v1.NodeGroupControllerAsyncClient()

                # Initialize request argument(s)
                request = dataproc_v1.ResizeNodeGroupRequest(
                    name="name_value",
                    size=443,
                )

                # Make the request
                operation = client.resize_node_group(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.dataproc_v1.types.ResizeNodeGroupRequest, dict]]):
                The request object. A request to resize a node group.
            name (:class:`str`):
                Required. The name of the node group to resize. Format:
                ``projects/{project}/regions/{region}/clusters/{cluster}/nodeGroups/{nodeGroup}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            size (:class:`int`):
                Required. The number of running
                instances for the node group to
                maintain. The group adds or removes
                instances to maintain the number of
                instances specified by this parameter.

                This corresponds to the ``size`` field
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

                The result type for the operation will be :class:`google.cloud.dataproc_v1.types.NodeGroup` Dataproc Node Group.
                   **The Dataproc NodeGroup resource is not related to
                   the Dataproc
                   [NodeGroupAffinity][google.cloud.dataproc.v1.NodeGroupAffinity]
                   resource.**

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, size])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = node_groups.ResizeNodeGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name
        if size is not None:
            request.size = size

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.resize_node_group,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            clusters.NodeGroup,
            metadata_type=operations.NodeGroupOperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_node_group(
        self,
        request: Optional[Union[node_groups.GetNodeGroupRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> clusters.NodeGroup:
        r"""Gets the resource representation for a node group in
        a cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import dataproc_v1

            async def sample_get_node_group():
                # Create a client
                client = dataproc_v1.NodeGroupControllerAsyncClient()

                # Initialize request argument(s)
                request = dataproc_v1.GetNodeGroupRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_node_group(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.dataproc_v1.types.GetNodeGroupRequest, dict]]):
                The request object. A request to get a node group .
            name (:class:`str`):
                Required. The name of the node group to retrieve.
                Format:
                ``projects/{project}/regions/{region}/clusters/{cluster}/nodeGroups/{nodeGroup}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataproc_v1.types.NodeGroup:
                Dataproc Node Group.
                   **The Dataproc NodeGroup resource is not related to
                   the Dataproc
                   [NodeGroupAffinity][google.cloud.dataproc.v1.NodeGroupAffinity]
                   resource.**

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

        request = node_groups.GetNodeGroupRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_node_group,
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


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("NodeGroupControllerAsyncClient",)
