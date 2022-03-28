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
from typing import Dict, Optional, Sequence, Tuple, Type, Union
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
from google.cloud.bigtable_admin_v2.services.bigtable_instance_admin import pagers
from google.cloud.bigtable_admin_v2.types import bigtable_instance_admin
from google.cloud.bigtable_admin_v2.types import common
from google.cloud.bigtable_admin_v2.types import instance
from google.cloud.bigtable_admin_v2.types import instance as gba_instance
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import BigtableInstanceAdminTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import BigtableInstanceAdminGrpcAsyncIOTransport
from .client import BigtableInstanceAdminClient


class BigtableInstanceAdminAsyncClient:
    """Service for creating, configuring, and deleting Cloud
    Bigtable Instances and Clusters. Provides access to the Instance
    and Cluster schemas only, not the tables' metadata or data
    stored in those tables.
    """

    _client: BigtableInstanceAdminClient

    DEFAULT_ENDPOINT = BigtableInstanceAdminClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = BigtableInstanceAdminClient.DEFAULT_MTLS_ENDPOINT

    app_profile_path = staticmethod(BigtableInstanceAdminClient.app_profile_path)
    parse_app_profile_path = staticmethod(
        BigtableInstanceAdminClient.parse_app_profile_path
    )
    cluster_path = staticmethod(BigtableInstanceAdminClient.cluster_path)
    parse_cluster_path = staticmethod(BigtableInstanceAdminClient.parse_cluster_path)
    crypto_key_path = staticmethod(BigtableInstanceAdminClient.crypto_key_path)
    parse_crypto_key_path = staticmethod(
        BigtableInstanceAdminClient.parse_crypto_key_path
    )
    hot_tablet_path = staticmethod(BigtableInstanceAdminClient.hot_tablet_path)
    parse_hot_tablet_path = staticmethod(
        BigtableInstanceAdminClient.parse_hot_tablet_path
    )
    instance_path = staticmethod(BigtableInstanceAdminClient.instance_path)
    parse_instance_path = staticmethod(BigtableInstanceAdminClient.parse_instance_path)
    table_path = staticmethod(BigtableInstanceAdminClient.table_path)
    parse_table_path = staticmethod(BigtableInstanceAdminClient.parse_table_path)
    common_billing_account_path = staticmethod(
        BigtableInstanceAdminClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        BigtableInstanceAdminClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(BigtableInstanceAdminClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        BigtableInstanceAdminClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        BigtableInstanceAdminClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        BigtableInstanceAdminClient.parse_common_organization_path
    )
    common_project_path = staticmethod(BigtableInstanceAdminClient.common_project_path)
    parse_common_project_path = staticmethod(
        BigtableInstanceAdminClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        BigtableInstanceAdminClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        BigtableInstanceAdminClient.parse_common_location_path
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
            BigtableInstanceAdminAsyncClient: The constructed client.
        """
        return BigtableInstanceAdminClient.from_service_account_info.__func__(BigtableInstanceAdminAsyncClient, info, *args, **kwargs)  # type: ignore

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
            BigtableInstanceAdminAsyncClient: The constructed client.
        """
        return BigtableInstanceAdminClient.from_service_account_file.__func__(BigtableInstanceAdminAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return BigtableInstanceAdminClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> BigtableInstanceAdminTransport:
        """Returns the transport used by the client instance.

        Returns:
            BigtableInstanceAdminTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(BigtableInstanceAdminClient).get_transport_class,
        type(BigtableInstanceAdminClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, BigtableInstanceAdminTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the bigtable instance admin client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.BigtableInstanceAdminTransport]): The
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
        self._client = BigtableInstanceAdminClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_instance(
        self,
        request: Union[bigtable_instance_admin.CreateInstanceRequest, dict] = None,
        *,
        parent: str = None,
        instance_id: str = None,
        instance: gba_instance.Instance = None,
        clusters: Dict[str, gba_instance.Cluster] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Create an instance within a project.

        Note that exactly one of Cluster.serve_nodes and
        Cluster.cluster_config.cluster_autoscaling_config can be set. If
        serve_nodes is set to non-zero, then the cluster is manually
        scaled. If cluster_config.cluster_autoscaling_config is
        non-empty, then autoscaling is enabled.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.CreateInstanceRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.CreateInstance.
            parent (:class:`str`):
                Required. The unique name of the project in which to
                create the new instance. Values are of the form
                ``projects/{project}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance_id (:class:`str`):
                Required. The ID to be used when referring to the new
                instance within its project, e.g., just ``myinstance``
                rather than ``projects/myproject/instances/myinstance``.

                This corresponds to the ``instance_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            instance (:class:`google.cloud.bigtable_admin_v2.types.Instance`):
                Required. The instance to create. Fields marked
                ``OutputOnly`` must be left blank.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            clusters (Dict[str, gba_instance.Cluster]):
                Required. The clusters to be created within the
                instance, mapped by desired cluster ID, e.g., just
                ``mycluster`` rather than
                ``projects/myproject/instances/myinstance/clusters/mycluster``.
                Fields marked ``OutputOnly`` must be left blank.
                Currently, at most four clusters can be specified.

                This corresponds to the ``clusters`` field
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

                The result type for the operation will be :class:`google.cloud.bigtable_admin_v2.types.Instance` A collection of Bigtable [Tables][google.bigtable.admin.v2.Table] and
                   the resources that serve them. All tables in an
                   instance are served from all
                   [Clusters][google.bigtable.admin.v2.Cluster] in the
                   instance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, instance_id, instance, clusters])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_instance_admin.CreateInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if instance_id is not None:
            request.instance_id = instance_id
        if instance is not None:
            request.instance = instance

        if clusters:
            request.clusters.update(clusters)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_instance,
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
            gba_instance.Instance,
            metadata_type=bigtable_instance_admin.CreateInstanceMetadata,
        )

        # Done; return the response.
        return response

    async def get_instance(
        self,
        request: Union[bigtable_instance_admin.GetInstanceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> instance.Instance:
        r"""Gets information about an instance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.GetInstanceRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.GetInstance.
            name (:class:`str`):
                Required. The unique name of the requested instance.
                Values are of the form
                ``projects/{project}/instances/{instance}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.Instance:
                A collection of Bigtable [Tables][google.bigtable.admin.v2.Table] and
                   the resources that serve them. All tables in an
                   instance are served from all
                   [Clusters][google.bigtable.admin.v2.Cluster] in the
                   instance.

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

        request = bigtable_instance_admin.GetInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_instance,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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

    async def list_instances(
        self,
        request: Union[bigtable_instance_admin.ListInstancesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable_instance_admin.ListInstancesResponse:
        r"""Lists information about instances in a project.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.ListInstancesRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.ListInstances.
            parent (:class:`str`):
                Required. The unique name of the project for which a
                list of instances is requested. Values are of the form
                ``projects/{project}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.ListInstancesResponse:
                Response message for
                BigtableInstanceAdmin.ListInstances.

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

        request = bigtable_instance_admin.ListInstancesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_instances,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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

    async def update_instance(
        self,
        request: Union[instance.Instance, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> instance.Instance:
        r"""Updates an instance within a project. This method
        updates only the display name and type for an Instance.
        To update other Instance properties, such as labels, use
        PartialUpdateInstance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.Instance, dict]):
                The request object. A collection of Bigtable
                [Tables][google.bigtable.admin.v2.Table] and the
                resources that serve them. All tables in an instance are
                served from all
                [Clusters][google.bigtable.admin.v2.Cluster] in the
                instance.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.Instance:
                A collection of Bigtable [Tables][google.bigtable.admin.v2.Table] and
                   the resources that serve them. All tables in an
                   instance are served from all
                   [Clusters][google.bigtable.admin.v2.Cluster] in the
                   instance.

        """
        # Create or coerce a protobuf request object.
        request = instance.Instance(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_instance,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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

    async def partial_update_instance(
        self,
        request: Union[
            bigtable_instance_admin.PartialUpdateInstanceRequest, dict
        ] = None,
        *,
        instance: gba_instance.Instance = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Partially updates an instance within a project. This
        method can modify all fields of an Instance and is the
        preferred way to update an Instance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.PartialUpdateInstanceRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.PartialUpdateInstance.
            instance (:class:`google.cloud.bigtable_admin_v2.types.Instance`):
                Required. The Instance which will
                (partially) replace the current value.

                This corresponds to the ``instance`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The subset of Instance
                fields which should be replaced. Must be
                explicitly set.

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

                The result type for the operation will be :class:`google.cloud.bigtable_admin_v2.types.Instance` A collection of Bigtable [Tables][google.bigtable.admin.v2.Table] and
                   the resources that serve them. All tables in an
                   instance are served from all
                   [Clusters][google.bigtable.admin.v2.Cluster] in the
                   instance.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([instance, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_instance_admin.PartialUpdateInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if instance is not None:
            request.instance = instance
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.partial_update_instance,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata(
                (("instance.name", request.instance.name),)
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
            gba_instance.Instance,
            metadata_type=bigtable_instance_admin.UpdateInstanceMetadata,
        )

        # Done; return the response.
        return response

    async def delete_instance(
        self,
        request: Union[bigtable_instance_admin.DeleteInstanceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Delete an instance from a project.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.DeleteInstanceRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.DeleteInstance.
            name (:class:`str`):
                Required. The unique name of the instance to be deleted.
                Values are of the form
                ``projects/{project}/instances/{instance}``.

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

        request = bigtable_instance_admin.DeleteInstanceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_instance,
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

    async def create_cluster(
        self,
        request: Union[bigtable_instance_admin.CreateClusterRequest, dict] = None,
        *,
        parent: str = None,
        cluster_id: str = None,
        cluster: instance.Cluster = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a cluster within an instance.

        Note that exactly one of Cluster.serve_nodes and
        Cluster.cluster_config.cluster_autoscaling_config can be set. If
        serve_nodes is set to non-zero, then the cluster is manually
        scaled. If cluster_config.cluster_autoscaling_config is
        non-empty, then autoscaling is enabled.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.CreateClusterRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.CreateCluster.
            parent (:class:`str`):
                Required. The unique name of the instance in which to
                create the new cluster. Values are of the form
                ``projects/{project}/instances/{instance}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster_id (:class:`str`):
                Required. The ID to be used when referring to the new
                cluster within its instance, e.g., just ``mycluster``
                rather than
                ``projects/myproject/instances/myinstance/clusters/mycluster``.

                This corresponds to the ``cluster_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            cluster (:class:`google.cloud.bigtable_admin_v2.types.Cluster`):
                Required. The cluster to be created. Fields marked
                ``OutputOnly`` must be left blank.

                This corresponds to the ``cluster`` field
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

                The result type for the operation will be :class:`google.cloud.bigtable_admin_v2.types.Cluster` A resizable group of nodes in a particular cloud location, capable
                   of serving all
                   [Tables][google.bigtable.admin.v2.Table] in the
                   parent [Instance][google.bigtable.admin.v2.Instance].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, cluster_id, cluster])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_instance_admin.CreateClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if cluster_id is not None:
            request.cluster_id = cluster_id
        if cluster is not None:
            request.cluster = cluster

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_cluster,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            instance.Cluster,
            metadata_type=bigtable_instance_admin.CreateClusterMetadata,
        )

        # Done; return the response.
        return response

    async def get_cluster(
        self,
        request: Union[bigtable_instance_admin.GetClusterRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> instance.Cluster:
        r"""Gets information about a cluster.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.GetClusterRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.GetCluster.
            name (:class:`str`):
                Required. The unique name of the requested cluster.
                Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.Cluster:
                A resizable group of nodes in a particular cloud location, capable
                   of serving all
                   [Tables][google.bigtable.admin.v2.Table] in the
                   parent [Instance][google.bigtable.admin.v2.Instance].

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

        request = bigtable_instance_admin.GetClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_cluster,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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

    async def list_clusters(
        self,
        request: Union[bigtable_instance_admin.ListClustersRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> bigtable_instance_admin.ListClustersResponse:
        r"""Lists information about clusters in an instance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.ListClustersRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.ListClusters.
            parent (:class:`str`):
                Required. The unique name of the instance for which a
                list of clusters is requested. Values are of the form
                ``projects/{project}/instances/{instance}``. Use
                ``{instance} = '-'`` to list Clusters for all Instances
                in a project, e.g., ``projects/myproject/instances/-``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.ListClustersResponse:
                Response message for
                BigtableInstanceAdmin.ListClusters.

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

        request = bigtable_instance_admin.ListClustersRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_clusters,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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

    async def update_cluster(
        self,
        request: Union[instance.Cluster, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates a cluster within an instance.

        Note that UpdateCluster does not support updating
        cluster_config.cluster_autoscaling_config. In order to update
        it, you must use PartialUpdateCluster.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.Cluster, dict]):
                The request object. A resizable group of nodes in a
                particular cloud location, capable of serving all
                [Tables][google.bigtable.admin.v2.Table] in the parent
                [Instance][google.bigtable.admin.v2.Instance].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.bigtable_admin_v2.types.Cluster` A resizable group of nodes in a particular cloud location, capable
                   of serving all
                   [Tables][google.bigtable.admin.v2.Table] in the
                   parent [Instance][google.bigtable.admin.v2.Instance].

        """
        # Create or coerce a protobuf request object.
        request = instance.Cluster(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_cluster,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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
            instance.Cluster,
            metadata_type=bigtable_instance_admin.UpdateClusterMetadata,
        )

        # Done; return the response.
        return response

    async def partial_update_cluster(
        self,
        request: Union[
            bigtable_instance_admin.PartialUpdateClusterRequest, dict
        ] = None,
        *,
        cluster: instance.Cluster = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Partially updates a cluster within a project. This method is the
        preferred way to update a Cluster.

        To enable and update autoscaling, set
        cluster_config.cluster_autoscaling_config. When autoscaling is
        enabled, serve_nodes is treated as an OUTPUT_ONLY field, meaning
        that updates to it are ignored. Note that an update cannot
        simultaneously set serve_nodes to non-zero and
        cluster_config.cluster_autoscaling_config to non-empty, and also
        specify both in the update_mask.

        To disable autoscaling, clear
        cluster_config.cluster_autoscaling_config, and explicitly set a
        serve_node count via the update_mask.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.PartialUpdateClusterRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.PartialUpdateCluster.
            cluster (:class:`google.cloud.bigtable_admin_v2.types.Cluster`):
                Required. The Cluster which contains the partial updates
                to be applied, subject to the update_mask.

                This corresponds to the ``cluster`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The subset of Cluster
                fields which should be replaced.

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

                The result type for the operation will be :class:`google.cloud.bigtable_admin_v2.types.Cluster` A resizable group of nodes in a particular cloud location, capable
                   of serving all
                   [Tables][google.bigtable.admin.v2.Table] in the
                   parent [Instance][google.bigtable.admin.v2.Instance].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([cluster, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_instance_admin.PartialUpdateClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if cluster is not None:
            request.cluster = cluster
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.partial_update_cluster,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata(
                (("cluster.name", request.cluster.name),)
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
            instance.Cluster,
            metadata_type=bigtable_instance_admin.PartialUpdateClusterMetadata,
        )

        # Done; return the response.
        return response

    async def delete_cluster(
        self,
        request: Union[bigtable_instance_admin.DeleteClusterRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a cluster from an instance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.DeleteClusterRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.DeleteCluster.
            name (:class:`str`):
                Required. The unique name of the cluster to be deleted.
                Values are of the form
                ``projects/{project}/instances/{instance}/clusters/{cluster}``.

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

        request = bigtable_instance_admin.DeleteClusterRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_cluster,
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

    async def create_app_profile(
        self,
        request: Union[bigtable_instance_admin.CreateAppProfileRequest, dict] = None,
        *,
        parent: str = None,
        app_profile_id: str = None,
        app_profile: instance.AppProfile = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> instance.AppProfile:
        r"""Creates an app profile within an instance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.CreateAppProfileRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.CreateAppProfile.
            parent (:class:`str`):
                Required. The unique name of the instance in which to
                create the new app profile. Values are of the form
                ``projects/{project}/instances/{instance}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile_id (:class:`str`):
                Required. The ID to be used when referring to the new
                app profile within its instance, e.g., just
                ``myprofile`` rather than
                ``projects/myproject/instances/myinstance/appProfiles/myprofile``.

                This corresponds to the ``app_profile_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            app_profile (:class:`google.cloud.bigtable_admin_v2.types.AppProfile`):
                Required. The app profile to be created. Fields marked
                ``OutputOnly`` will be ignored.

                This corresponds to the ``app_profile`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.AppProfile:
                A configuration object describing how
                Cloud Bigtable should treat traffic from
                a particular end user application.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, app_profile_id, app_profile])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_instance_admin.CreateAppProfileRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if app_profile_id is not None:
            request.app_profile_id = app_profile_id
        if app_profile is not None:
            request.app_profile = app_profile

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_app_profile,
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

    async def get_app_profile(
        self,
        request: Union[bigtable_instance_admin.GetAppProfileRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> instance.AppProfile:
        r"""Gets information about an app profile.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.GetAppProfileRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.GetAppProfile.
            name (:class:`str`):
                Required. The unique name of the requested app profile.
                Values are of the form
                ``projects/{project}/instances/{instance}/appProfiles/{app_profile}``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.types.AppProfile:
                A configuration object describing how
                Cloud Bigtable should treat traffic from
                a particular end user application.

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

        request = bigtable_instance_admin.GetAppProfileRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_app_profile,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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

    async def list_app_profiles(
        self,
        request: Union[bigtable_instance_admin.ListAppProfilesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAppProfilesAsyncPager:
        r"""Lists information about app profiles in an instance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.ListAppProfilesRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.ListAppProfiles.
            parent (:class:`str`):
                Required. The unique name of the instance for which a
                list of app profiles is requested. Values are of the
                form ``projects/{project}/instances/{instance}``. Use
                ``{instance} = '-'`` to list AppProfiles for all
                Instances in a project, e.g.,
                ``projects/myproject/instances/-``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.services.bigtable_instance_admin.pagers.ListAppProfilesAsyncPager:
                Response message for
                BigtableInstanceAdmin.ListAppProfiles.
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

        request = bigtable_instance_admin.ListAppProfilesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_app_profiles,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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
        response = pagers.ListAppProfilesAsyncPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_app_profile(
        self,
        request: Union[bigtable_instance_admin.UpdateAppProfileRequest, dict] = None,
        *,
        app_profile: instance.AppProfile = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates an app profile within an instance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.UpdateAppProfileRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.UpdateAppProfile.
            app_profile (:class:`google.cloud.bigtable_admin_v2.types.AppProfile`):
                Required. The app profile which will
                (partially) replace the current value.

                This corresponds to the ``app_profile`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The subset of app profile
                fields which should be replaced. If
                unset, all fields will be replaced.

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

                The result type for the operation will be :class:`google.cloud.bigtable_admin_v2.types.AppProfile` A configuration object describing how Cloud Bigtable should treat traffic
                   from a particular end user application.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([app_profile, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = bigtable_instance_admin.UpdateAppProfileRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if app_profile is not None:
            request.app_profile = app_profile
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_app_profile,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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
            gapic_v1.routing_header.to_grpc_metadata(
                (("app_profile.name", request.app_profile.name),)
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
            instance.AppProfile,
            metadata_type=bigtable_instance_admin.UpdateAppProfileMetadata,
        )

        # Done; return the response.
        return response

    async def delete_app_profile(
        self,
        request: Union[bigtable_instance_admin.DeleteAppProfileRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an app profile from an instance.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.DeleteAppProfileRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.DeleteAppProfile.
            name (:class:`str`):
                Required. The unique name of the app profile to be
                deleted. Values are of the form
                ``projects/{project}/instances/{instance}/appProfiles/{app_profile}``.

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

        request = bigtable_instance_admin.DeleteAppProfileRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_app_profile,
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

    async def get_iam_policy(
        self,
        request: Union[iam_policy_pb2.GetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy for an instance
        resource. Returns an empty policy if an instance exists
        but does not have a policy set.

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]):
                The request object. Request message for `GetIamPolicy`
                method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy. It is used to
                   specify access control policies for Cloud Platform
                   resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions (defined by IAM or configured by users).
                   A binding can optionally specify a condition, which
                   is a logic expression that further constrains the
                   role binding based on attributes about the request
                   and/or target resource.

                   **JSON Example**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": ["user:eve@example.com"],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ]

                      }

                   **YAML Example**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z')

                   For a description of IAM and its features, see the
                   [IAM developer's
                   guide](\ https://cloud.google.com/iam/docs).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy_pb2.GetIamPolicyRequest(
                resource=resource,
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_iam_policy,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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

    async def set_iam_policy(
        self,
        request: Union[iam_policy_pb2.SetIamPolicyRequest, dict] = None,
        *,
        resource: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the access control policy on an instance
        resource. Replaces any existing policy.

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]):
                The request object. Request message for `SetIamPolicy`
                method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                Defines an Identity and Access Management (IAM) policy. It is used to
                   specify access control policies for Cloud Platform
                   resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members to a single role. Members can be
                   user accounts, service accounts, Google groups, and
                   domains (such as G Suite). A role is a named list of
                   permissions (defined by IAM or configured by users).
                   A binding can optionally specify a condition, which
                   is a logic expression that further constrains the
                   role binding based on attributes about the request
                   and/or target resource.

                   **JSON Example**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": ["user:eve@example.com"],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ]

                      }

                   **YAML Example**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z')

                   For a description of IAM and its features, see the
                   [IAM developer's
                   guide](\ https://cloud.google.com/iam/docs).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            request = iam_policy_pb2.SetIamPolicyRequest(
                resource=resource,
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.set_iam_policy,
            default_timeout=60.0,
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
        request: Union[iam_policy_pb2.TestIamPermissionsRequest, dict] = None,
        *,
        resource: str = None,
        permissions: Sequence[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns permissions that the caller has on the
        specified instance resource.

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for
                `TestIamPermissions` method.
            resource (:class:`str`):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (:class:`Sequence[str]`):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, permissions])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            request = iam_policy_pb2.TestIamPermissionsRequest(
                resource=resource,
                permissions=permissions,
            )

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.test_iam_permissions,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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

    async def list_hot_tablets(
        self,
        request: Union[bigtable_instance_admin.ListHotTabletsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListHotTabletsAsyncPager:
        r"""Lists hot tablets in a cluster, within the time range
        provided. Hot tablets are ordered based on CPU usage.

        Args:
            request (Union[google.cloud.bigtable_admin_v2.types.ListHotTabletsRequest, dict]):
                The request object. Request message for
                BigtableInstanceAdmin.ListHotTablets.
            parent (:class:`str`):
                Required. The cluster name to list hot tablets. Value is
                in the following form:
                ``projects/{project}/instances/{instance}/clusters/{cluster}``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigtable_admin_v2.services.bigtable_instance_admin.pagers.ListHotTabletsAsyncPager:
                Response message for
                BigtableInstanceAdmin.ListHotTablets.
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

        request = bigtable_instance_admin.ListHotTabletsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_hot_tablets,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
                multiplier=2,
                predicate=retries.if_exception_type(
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
        response = pagers.ListHotTabletsAsyncPager(
            method=rpc,
            request=request,
            response=response,
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
            "google-cloud-bigtable-admin",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("BigtableInstanceAdminAsyncClient",)
