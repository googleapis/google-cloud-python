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

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry_async as retries
from google.api_core.client_options import ClientOptions
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.gke_multicloud_v1 import gapic_version as package_version

try:
    OptionalRetry = Union[retries.AsyncRetry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.AsyncRetry, object, None]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore

from google.cloud.gke_multicloud_v1.services.attached_clusters import pagers
from google.cloud.gke_multicloud_v1.types import (
    attached_resources,
    attached_service,
    common_resources,
)

from .client import AttachedClustersClient
from .transports.base import DEFAULT_CLIENT_INFO, AttachedClustersTransport
from .transports.grpc_asyncio import AttachedClustersGrpcAsyncIOTransport


class AttachedClustersAsyncClient:
    """The AttachedClusters API provides a single centrally managed
    service to register and manage Anthos attached clusters that run
    on customer's owned infrastructure.
    """

    _client: AttachedClustersClient

    # Copy defaults from the synchronous client for use here.
    # Note: DEFAULT_ENDPOINT is deprecated. Use _DEFAULT_ENDPOINT_TEMPLATE instead.
    DEFAULT_ENDPOINT = AttachedClustersClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = AttachedClustersClient.DEFAULT_MTLS_ENDPOINT
    _DEFAULT_ENDPOINT_TEMPLATE = AttachedClustersClient._DEFAULT_ENDPOINT_TEMPLATE
    _DEFAULT_UNIVERSE = AttachedClustersClient._DEFAULT_UNIVERSE

    attached_cluster_path = staticmethod(AttachedClustersClient.attached_cluster_path)
    parse_attached_cluster_path = staticmethod(
        AttachedClustersClient.parse_attached_cluster_path
    )
    attached_server_config_path = staticmethod(
        AttachedClustersClient.attached_server_config_path
    )
    parse_attached_server_config_path = staticmethod(
        AttachedClustersClient.parse_attached_server_config_path
    )
    common_billing_account_path = staticmethod(
        AttachedClustersClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        AttachedClustersClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(AttachedClustersClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        AttachedClustersClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        AttachedClustersClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        AttachedClustersClient.parse_common_organization_path
    )
    common_project_path = staticmethod(AttachedClustersClient.common_project_path)
    parse_common_project_path = staticmethod(
        AttachedClustersClient.parse_common_project_path
    )
    common_location_path = staticmethod(AttachedClustersClient.common_location_path)
    parse_common_location_path = staticmethod(
        AttachedClustersClient.parse_common_location_path
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
            AttachedClustersAsyncClient: The constructed client.
        """
        return AttachedClustersClient.from_service_account_info.__func__(AttachedClustersAsyncClient, info, *args, **kwargs)  # type: ignore

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
            AttachedClustersAsyncClient: The constructed client.
        """
        return AttachedClustersClient.from_service_account_file.__func__(AttachedClustersAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return AttachedClustersClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> AttachedClustersTransport:
        """Returns the transport used by the client instance.

        Returns:
            AttachedClustersTransport: The transport used by the client instance.
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

    get_transport_class = AttachedClustersClient.get_transport_class

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[
            Union[
                str, AttachedClustersTransport, Callable[..., AttachedClustersTransport]
            ]
        ] = "grpc_asyncio",
        client_options: Optional[ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the attached clusters async client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Optional[Union[str,AttachedClustersTransport,Callable[..., AttachedClustersTransport]]]):
                The transport to use, or a Callable that constructs and returns a new transport to use.
                If a Callable is given, it will be called with the same set of initialization
                arguments as used in the AttachedClustersTransport constructor.
                If set to None, a transport is chosen automatically.
                NOTE: "rest" transport functionality is currently in a
                beta state (preview). We welcome your feedback via an
                issue in this library's source repository.
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
        self._client = AttachedClustersClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_attached_cluster(
        self,
        request: Optional[
            Union[attached_service.CreateAttachedClusterRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        attached_cluster: Optional[attached_resources.AttachedCluster] = None,
        attached_cluster_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new
        [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
        resource on a given Google Cloud Platform project and region.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            async def sample_create_attached_cluster():
                # Create a client
                client = gke_multicloud_v1.AttachedClustersAsyncClient()

                # Initialize request argument(s)
                attached_cluster = gke_multicloud_v1.AttachedCluster()
                attached_cluster.platform_version = "platform_version_value"
                attached_cluster.distribution = "distribution_value"
                attached_cluster.fleet.project = "project_value"

                request = gke_multicloud_v1.CreateAttachedClusterRequest(
                    parent="parent_value",
                    attached_cluster=attached_cluster,
                    attached_cluster_id="attached_cluster_id_value",
                )

                # Make the request
                operation = client.create_attached_cluster(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.gke_multicloud_v1.types.CreateAttachedClusterRequest, dict]]):
                The request object. Request message for
                ``AttachedClusters.CreateAttachedCluster`` method.
            parent (:class:`str`):
                Required. The parent location where this
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
                resource will be created.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            attached_cluster (:class:`google.cloud.gke_multicloud_v1.types.AttachedCluster`):
                Required. The specification of the
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
                to create.

                This corresponds to the ``attached_cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            attached_cluster_id (:class:`str`):
                Required. A client provided ID the resource. Must be
                unique within the parent resource.

                The provided ID will be part of the
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
                resource name formatted as
                ``projects/<project-id>/locations/<region>/attachedClusters/<cluster-id>``.

                Valid characters are ``/[a-z][0-9]-/``. Cannot be longer
                than 63 characters.

                This corresponds to the ``attached_cluster_id`` field
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

                The result type for the operation will be
                :class:`google.cloud.gke_multicloud_v1.types.AttachedCluster`
                An Anthos cluster running on customer own
                infrastructure.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, attached_cluster, attached_cluster_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, attached_service.CreateAttachedClusterRequest):
            request = attached_service.CreateAttachedClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if attached_cluster is not None:
            request.attached_cluster = attached_cluster
        if attached_cluster_id is not None:
            request.attached_cluster_id = attached_cluster_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.create_attached_cluster
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

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
            attached_resources.AttachedCluster,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_attached_cluster(
        self,
        request: Optional[
            Union[attached_service.UpdateAttachedClusterRequest, dict]
        ] = None,
        *,
        attached_cluster: Optional[attached_resources.AttachedCluster] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates an
        [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            async def sample_update_attached_cluster():
                # Create a client
                client = gke_multicloud_v1.AttachedClustersAsyncClient()

                # Initialize request argument(s)
                attached_cluster = gke_multicloud_v1.AttachedCluster()
                attached_cluster.platform_version = "platform_version_value"
                attached_cluster.distribution = "distribution_value"
                attached_cluster.fleet.project = "project_value"

                request = gke_multicloud_v1.UpdateAttachedClusterRequest(
                    attached_cluster=attached_cluster,
                )

                # Make the request
                operation = client.update_attached_cluster(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.gke_multicloud_v1.types.UpdateAttachedClusterRequest, dict]]):
                The request object. Request message for
                ``AttachedClusters.UpdateAttachedCluster`` method.
            attached_cluster (:class:`google.cloud.gke_multicloud_v1.types.AttachedCluster`):
                Required. The
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
                resource to update.

                This corresponds to the ``attached_cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Mask of fields to update. At least one path
                must be supplied in this field. The elements of the
                repeated paths field can only include these fields from
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]:

                -  ``annotations``.
                -  ``authorization.admin_groups``.
                -  ``authorization.admin_users``.
                -  ``binary_authorization.evaluation_mode``.
                -  ``description``.
                -  ``logging_config.component_config.enable_components``.
                -  ``monitoring_config.managed_prometheus_config.enabled``.
                -  ``platform_version``.
                -  ``proxy_config.kubernetes_secret.name``.
                -  ``proxy_config.kubernetes_secret.namespace``.
                -  ``security_posture_config.vulnerability_mode``

                This corresponds to the ``update_mask`` field
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

                The result type for the operation will be
                :class:`google.cloud.gke_multicloud_v1.types.AttachedCluster`
                An Anthos cluster running on customer own
                infrastructure.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([attached_cluster, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, attached_service.UpdateAttachedClusterRequest):
            request = attached_service.UpdateAttachedClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if attached_cluster is not None:
            request.attached_cluster = attached_cluster
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.update_attached_cluster
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("attached_cluster.name", request.attached_cluster.name),)
            ),
        )

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
            attached_resources.AttachedCluster,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def import_attached_cluster(
        self,
        request: Optional[
            Union[attached_service.ImportAttachedClusterRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        fleet_membership: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Imports creates a new
        [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
        resource by importing an existing Fleet Membership resource.

        Attached Clusters created before the introduction of the Anthos
        Multi-Cloud API can be imported through this method.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            async def sample_import_attached_cluster():
                # Create a client
                client = gke_multicloud_v1.AttachedClustersAsyncClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.ImportAttachedClusterRequest(
                    parent="parent_value",
                    fleet_membership="fleet_membership_value",
                    platform_version="platform_version_value",
                    distribution="distribution_value",
                )

                # Make the request
                operation = client.import_attached_cluster(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.gke_multicloud_v1.types.ImportAttachedClusterRequest, dict]]):
                The request object. Request message for
                ``AttachedClusters.ImportAttachedCluster`` method.
            parent (:class:`str`):
                Required. The parent location where this
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
                resource will be created.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            fleet_membership (:class:`str`):
                Required. The name of the fleet
                membership resource to import.

                This corresponds to the ``fleet_membership`` field
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

                The result type for the operation will be
                :class:`google.cloud.gke_multicloud_v1.types.AttachedCluster`
                An Anthos cluster running on customer own
                infrastructure.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, fleet_membership])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(request, attached_service.ImportAttachedClusterRequest):
            request = attached_service.ImportAttachedClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if fleet_membership is not None:
            request.fleet_membership = fleet_membership

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.import_attached_cluster
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

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
            attached_resources.AttachedCluster,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_attached_cluster(
        self,
        request: Optional[
            Union[attached_service.GetAttachedClusterRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> attached_resources.AttachedCluster:
        r"""Describes a specific
        [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
        resource.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            async def sample_get_attached_cluster():
                # Create a client
                client = gke_multicloud_v1.AttachedClustersAsyncClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GetAttachedClusterRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_attached_cluster(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.gke_multicloud_v1.types.GetAttachedClusterRequest, dict]]):
                The request object. Request message for
                ``AttachedClusters.GetAttachedCluster`` method.
            name (:class:`str`):
                Required. The name of the
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
                resource to describe.

                ``AttachedCluster`` names are formatted as
                ``projects/<project-id>/locations/<region>/attachedClusters/<cluster-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud Platform resource
                names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.AttachedCluster:
                An Anthos cluster running on customer
                own infrastructure.

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
        if not isinstance(request, attached_service.GetAttachedClusterRequest):
            request = attached_service.GetAttachedClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.get_attached_cluster
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

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

    async def list_attached_clusters(
        self,
        request: Optional[
            Union[attached_service.ListAttachedClustersRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAttachedClustersAsyncPager:
        r"""Lists all
        [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
        resources on a given Google Cloud project and region.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            async def sample_list_attached_clusters():
                # Create a client
                client = gke_multicloud_v1.AttachedClustersAsyncClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.ListAttachedClustersRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_attached_clusters(request=request)

                # Handle the response
                async for response in page_result:
                    print(response)

        Args:
            request (Optional[Union[google.cloud.gke_multicloud_v1.types.ListAttachedClustersRequest, dict]]):
                The request object. Request message for
                ``AttachedClusters.ListAttachedClusters`` method.
            parent (:class:`str`):
                Required. The parent location which owns this collection
                of
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
                resources.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud Platform resource
                names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.services.attached_clusters.pagers.ListAttachedClustersAsyncPager:
                Response message for
                AttachedClusters.ListAttachedClusters method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

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
        if not isinstance(request, attached_service.ListAttachedClustersRequest):
            request = attached_service.ListAttachedClustersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.list_attached_clusters
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

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
        response = pagers.ListAttachedClustersAsyncPager(
            method=rpc,
            request=request,
            response=response,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_attached_cluster(
        self,
        request: Optional[
            Union[attached_service.DeleteAttachedClusterRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a specific
        [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
        resource.

        If successful, the response contains a newly created
        [Operation][google.longrunning.Operation] resource that can be
        described to track the status of the operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            async def sample_delete_attached_cluster():
                # Create a client
                client = gke_multicloud_v1.AttachedClustersAsyncClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.DeleteAttachedClusterRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_attached_cluster(request=request)

                print("Waiting for operation to complete...")

                response = (await operation).result()

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.gke_multicloud_v1.types.DeleteAttachedClusterRequest, dict]]):
                The request object. Request message for
                ``AttachedClusters.DeleteAttachedCluster`` method.
            name (:class:`str`):
                Required. The resource name the
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
                to delete.

                ``AttachedCluster`` names are formatted as
                ``projects/<project-id>/locations/<region>/attachedClusters/<cluster-id>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud Platform resource
                names.

                This corresponds to the ``name`` field
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

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

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
        if not isinstance(request, attached_service.DeleteAttachedClusterRequest):
            request = attached_service.DeleteAttachedClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.delete_attached_cluster
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

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
            empty_pb2.Empty,
            metadata_type=common_resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_attached_server_config(
        self,
        request: Optional[
            Union[attached_service.GetAttachedServerConfigRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> attached_resources.AttachedServerConfig:
        r"""Returns information, such as supported Kubernetes
        versions, on a given Google Cloud location.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            async def sample_get_attached_server_config():
                # Create a client
                client = gke_multicloud_v1.AttachedClustersAsyncClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GetAttachedServerConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = await client.get_attached_server_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.gke_multicloud_v1.types.GetAttachedServerConfigRequest, dict]]):
                The request object. GetAttachedServerConfigRequest gets
                the server config for attached clusters.
            name (:class:`str`):
                Required. The name of the
                [AttachedServerConfig][google.cloud.gkemulticloud.v1.AttachedServerConfig]
                resource to describe.

                ``AttachedServerConfig`` names are formatted as
                ``projects/<project-id>/locations/<region>/attachedServerConfig``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.AttachedServerConfig:
                AttachedServerConfig provides
                information about supported Kubernetes
                versions

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
        if not isinstance(request, attached_service.GetAttachedServerConfigRequest):
            request = attached_service.GetAttachedServerConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.get_attached_server_config
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

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

    async def generate_attached_cluster_install_manifest(
        self,
        request: Optional[
            Union[attached_service.GenerateAttachedClusterInstallManifestRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        attached_cluster_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> attached_service.GenerateAttachedClusterInstallManifestResponse:
        r"""Generates the install manifest to be installed on the
        target cluster.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            async def sample_generate_attached_cluster_install_manifest():
                # Create a client
                client = gke_multicloud_v1.AttachedClustersAsyncClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GenerateAttachedClusterInstallManifestRequest(
                    parent="parent_value",
                    attached_cluster_id="attached_cluster_id_value",
                    platform_version="platform_version_value",
                )

                # Make the request
                response = await client.generate_attached_cluster_install_manifest(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.gke_multicloud_v1.types.GenerateAttachedClusterInstallManifestRequest, dict]]):
                The request object. Request message for
                ``AttachedClusters.GenerateAttachedClusterInstallManifest``
                method.
            parent (:class:`str`):
                Required. The parent location where this
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
                resource will be created.

                Location names are formatted as
                ``projects/<project-id>/locations/<region>``.

                See `Resource
                Names <https://cloud.google.com/apis/design/resource_names>`__
                for more details on Google Cloud resource names.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            attached_cluster_id (:class:`str`):
                Required. A client provided ID of the resource. Must be
                unique within the parent resource.

                The provided ID will be part of the
                [AttachedCluster][google.cloud.gkemulticloud.v1.AttachedCluster]
                resource name formatted as
                ``projects/<project-id>/locations/<region>/attachedClusters/<cluster-id>``.

                Valid characters are ``/[a-z][0-9]-/``. Cannot be longer
                than 63 characters.

                When generating an install manifest for importing an
                existing Membership resource, the attached_cluster_id
                field must be the Membership id.

                Membership names are formatted as
                ``projects/<project-id>/locations/<region>/memberships/<membership-id>``.

                This corresponds to the ``attached_cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.GenerateAttachedClusterInstallManifestResponse:
                Response message for
                   AttachedClusters.GenerateAttachedClusterInstallManifest
                   method.

        """
        # Create or coerce a protobuf request object.
        # - Quick check: If we got a request object, we should *not* have
        #   gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, attached_cluster_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, attached_service.GenerateAttachedClusterInstallManifestRequest
        ):
            request = attached_service.GenerateAttachedClusterInstallManifestRequest(
                request
            )

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if attached_cluster_id is not None:
            request.attached_cluster_id = attached_cluster_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.generate_attached_cluster_install_manifest
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

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

    async def generate_attached_cluster_agent_token(
        self,
        request: Optional[
            Union[attached_service.GenerateAttachedClusterAgentTokenRequest, dict]
        ] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> attached_service.GenerateAttachedClusterAgentTokenResponse:
        r"""Generates an access token for a cluster agent.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import gke_multicloud_v1

            async def sample_generate_attached_cluster_agent_token():
                # Create a client
                client = gke_multicloud_v1.AttachedClustersAsyncClient()

                # Initialize request argument(s)
                request = gke_multicloud_v1.GenerateAttachedClusterAgentTokenRequest(
                    attached_cluster="attached_cluster_value",
                    subject_token="subject_token_value",
                    subject_token_type="subject_token_type_value",
                    version="version_value",
                )

                # Make the request
                response = await client.generate_attached_cluster_agent_token(request=request)

                # Handle the response
                print(response)

        Args:
            request (Optional[Union[google.cloud.gke_multicloud_v1.types.GenerateAttachedClusterAgentTokenRequest, dict]]):
                The request object.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.gke_multicloud_v1.types.GenerateAttachedClusterAgentTokenResponse:

        """
        # Create or coerce a protobuf request object.
        # - Use the request object if provided (there's no risk of modifying the input as
        #   there are no flattened fields), or create one.
        if not isinstance(
            request, attached_service.GenerateAttachedClusterAgentTokenRequest
        ):
            request = attached_service.GenerateAttachedClusterAgentTokenRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._client._transport._wrapped_methods[
            self._client._transport.generate_attached_cluster_agent_token
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("attached_cluster", request.attached_cluster),)
            ),
        )

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

    async def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_operations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

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

    async def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

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

    async def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry_async.AsyncRetry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Validate the universe domain.
        self._client._validate_universe_domain()

        # Send the request.
        await rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    async def __aenter__(self) -> "AttachedClustersAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("AttachedClustersAsyncClient",)
