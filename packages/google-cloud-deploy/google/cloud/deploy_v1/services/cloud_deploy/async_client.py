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
from google.cloud.deploy_v1.services.cloud_deploy import pagers
from google.cloud.deploy_v1.types import cloud_deploy
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import CloudDeployTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import CloudDeployGrpcAsyncIOTransport
from .client import CloudDeployClient


class CloudDeployAsyncClient:
    """CloudDeploy service creates and manages Continuous Delivery
    operations on Google Cloud Platform via Skaffold
    (https://skaffold.dev).
    """

    _client: CloudDeployClient

    DEFAULT_ENDPOINT = CloudDeployClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = CloudDeployClient.DEFAULT_MTLS_ENDPOINT

    build_path = staticmethod(CloudDeployClient.build_path)
    parse_build_path = staticmethod(CloudDeployClient.parse_build_path)
    cluster_path = staticmethod(CloudDeployClient.cluster_path)
    parse_cluster_path = staticmethod(CloudDeployClient.parse_cluster_path)
    config_path = staticmethod(CloudDeployClient.config_path)
    parse_config_path = staticmethod(CloudDeployClient.parse_config_path)
    delivery_pipeline_path = staticmethod(CloudDeployClient.delivery_pipeline_path)
    parse_delivery_pipeline_path = staticmethod(
        CloudDeployClient.parse_delivery_pipeline_path
    )
    release_path = staticmethod(CloudDeployClient.release_path)
    parse_release_path = staticmethod(CloudDeployClient.parse_release_path)
    rollout_path = staticmethod(CloudDeployClient.rollout_path)
    parse_rollout_path = staticmethod(CloudDeployClient.parse_rollout_path)
    target_path = staticmethod(CloudDeployClient.target_path)
    parse_target_path = staticmethod(CloudDeployClient.parse_target_path)
    worker_pool_path = staticmethod(CloudDeployClient.worker_pool_path)
    parse_worker_pool_path = staticmethod(CloudDeployClient.parse_worker_pool_path)
    common_billing_account_path = staticmethod(
        CloudDeployClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        CloudDeployClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(CloudDeployClient.common_folder_path)
    parse_common_folder_path = staticmethod(CloudDeployClient.parse_common_folder_path)
    common_organization_path = staticmethod(CloudDeployClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        CloudDeployClient.parse_common_organization_path
    )
    common_project_path = staticmethod(CloudDeployClient.common_project_path)
    parse_common_project_path = staticmethod(
        CloudDeployClient.parse_common_project_path
    )
    common_location_path = staticmethod(CloudDeployClient.common_location_path)
    parse_common_location_path = staticmethod(
        CloudDeployClient.parse_common_location_path
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
            CloudDeployAsyncClient: The constructed client.
        """
        return CloudDeployClient.from_service_account_info.__func__(CloudDeployAsyncClient, info, *args, **kwargs)  # type: ignore

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
            CloudDeployAsyncClient: The constructed client.
        """
        return CloudDeployClient.from_service_account_file.__func__(CloudDeployAsyncClient, filename, *args, **kwargs)  # type: ignore

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
        return CloudDeployClient.get_mtls_endpoint_and_cert_source(client_options)  # type: ignore

    @property
    def transport(self) -> CloudDeployTransport:
        """Returns the transport used by the client instance.

        Returns:
            CloudDeployTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(CloudDeployClient).get_transport_class, type(CloudDeployClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, CloudDeployTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the cloud deploy client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.CloudDeployTransport]): The
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
        self._client = CloudDeployClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_delivery_pipelines(
        self,
        request: Union[cloud_deploy.ListDeliveryPipelinesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDeliveryPipelinesAsyncPager:
        r"""Lists DeliveryPipelines in a given project and
        location.


        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_list_delivery_pipelines():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ListDeliveryPipelinesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_delivery_pipelines(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ListDeliveryPipelinesRequest, dict]):
                The request object. The request object for
                `ListDeliveryPipelines`.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                pipelines. Format must be
                projects/{project_id}/locations/{location_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.services.cloud_deploy.pagers.ListDeliveryPipelinesAsyncPager:
                The response object from ListDeliveryPipelines.

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

        request = cloud_deploy.ListDeliveryPipelinesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_delivery_pipelines,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
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
        response = pagers.ListDeliveryPipelinesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_delivery_pipeline(
        self,
        request: Union[cloud_deploy.GetDeliveryPipelineRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.DeliveryPipeline:
        r"""Gets details of a single DeliveryPipeline.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_get_delivery_pipeline():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetDeliveryPipelineRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_delivery_pipeline(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetDeliveryPipelineRequest, dict]):
                The request object. The request object for
                `GetDeliveryPipeline`
            name (:class:`str`):
                Required. Name of the ``DeliveryPipeline``. Format must
                be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.DeliveryPipeline:
                A DeliveryPipeline resource in the Google Cloud Deploy
                API.

                   A DeliveryPipeline defines a pipeline through which a
                   Skaffold configuration can progress.

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

        request = cloud_deploy.GetDeliveryPipelineRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_delivery_pipeline,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
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

    async def create_delivery_pipeline(
        self,
        request: Union[cloud_deploy.CreateDeliveryPipelineRequest, dict] = None,
        *,
        parent: str = None,
        delivery_pipeline: cloud_deploy.DeliveryPipeline = None,
        delivery_pipeline_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new DeliveryPipeline in a given project and
        location.


        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_create_delivery_pipeline():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.CreateDeliveryPipelineRequest(
                    parent="parent_value",
                    delivery_pipeline_id="delivery_pipeline_id_value",
                )

                # Make the request
                operation = client.create_delivery_pipeline(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.CreateDeliveryPipelineRequest, dict]):
                The request object. The request object for
                `CreateDeliveryPipeline`.
            parent (:class:`str`):
                Required. The parent collection in which the
                ``DeliveryPipeline`` should be created. Format should be
                projects/{project_id}/locations/{location_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            delivery_pipeline (:class:`google.cloud.deploy_v1.types.DeliveryPipeline`):
                Required. The ``DeliveryPipeline`` to create.
                This corresponds to the ``delivery_pipeline`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            delivery_pipeline_id (:class:`str`):
                Required. ID of the ``DeliveryPipeline``.
                This corresponds to the ``delivery_pipeline_id`` field
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
                :class:`google.cloud.deploy_v1.types.DeliveryPipeline` A
                DeliveryPipeline resource in the Google Cloud Deploy
                API.

                   A DeliveryPipeline defines a pipeline through which a
                   Skaffold configuration can progress.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, delivery_pipeline, delivery_pipeline_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_deploy.CreateDeliveryPipelineRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if delivery_pipeline is not None:
            request.delivery_pipeline = delivery_pipeline
        if delivery_pipeline_id is not None:
            request.delivery_pipeline_id = delivery_pipeline_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_delivery_pipeline,
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
            cloud_deploy.DeliveryPipeline,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_delivery_pipeline(
        self,
        request: Union[cloud_deploy.UpdateDeliveryPipelineRequest, dict] = None,
        *,
        delivery_pipeline: cloud_deploy.DeliveryPipeline = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single DeliveryPipeline.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_update_delivery_pipeline():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.UpdateDeliveryPipelineRequest(
                )

                # Make the request
                operation = client.update_delivery_pipeline(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.UpdateDeliveryPipelineRequest, dict]):
                The request object. The request object for
                `UpdateDeliveryPipeline`.
            delivery_pipeline (:class:`google.cloud.deploy_v1.types.DeliveryPipeline`):
                Required. The ``DeliveryPipeline`` to update.
                This corresponds to the ``delivery_pipeline`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Field mask is used to specify the fields to be
                overwritten in the ``DeliveryPipeline`` resource by the
                update. The fields specified in the update_mask are
                relative to the resource, not the full request. A field
                will be overwritten if it is in the mask. If the user
                does not provide a mask then all fields will be
                overwritten.

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
                :class:`google.cloud.deploy_v1.types.DeliveryPipeline` A
                DeliveryPipeline resource in the Google Cloud Deploy
                API.

                   A DeliveryPipeline defines a pipeline through which a
                   Skaffold configuration can progress.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([delivery_pipeline, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_deploy.UpdateDeliveryPipelineRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if delivery_pipeline is not None:
            request.delivery_pipeline = delivery_pipeline
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_delivery_pipeline,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("delivery_pipeline.name", request.delivery_pipeline.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_deploy.DeliveryPipeline,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_delivery_pipeline(
        self,
        request: Union[cloud_deploy.DeleteDeliveryPipelineRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single DeliveryPipeline.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_delete_delivery_pipeline():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.DeleteDeliveryPipelineRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_delivery_pipeline(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.DeleteDeliveryPipelineRequest, dict]):
                The request object. The request object for
                `DeleteDeliveryPipeline`.
            name (:class:`str`):
                Required. The name of the ``DeliveryPipeline`` to
                delete. Format should be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_deploy.DeleteDeliveryPipelineRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_delivery_pipeline,
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
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_targets(
        self,
        request: Union[cloud_deploy.ListTargetsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListTargetsAsyncPager:
        r"""Lists Targets in a given project and location.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_list_targets():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ListTargetsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_targets(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ListTargetsRequest, dict]):
                The request object. The request object for
                `ListTargets`.
            parent (:class:`str`):
                Required. The parent, which owns this collection of
                targets. Format must be
                projects/{project_id}/locations/{location_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.services.cloud_deploy.pagers.ListTargetsAsyncPager:
                The response object from ListTargets.

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

        request = cloud_deploy.ListTargetsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_targets,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
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
        response = pagers.ListTargetsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_target(
        self,
        request: Union[cloud_deploy.GetTargetRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.Target:
        r"""Gets details of a single Target.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_get_target():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetTargetRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_target(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetTargetRequest, dict]):
                The request object. The request object for `GetTarget`.
            name (:class:`str`):
                Required. Name of the ``Target``. Format must be
                projects/{project_id}/locations/{location_name}/targets/{target_name}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.Target:
                A Target resource in the Google Cloud Deploy API.

                   A Target defines a location to which a Skaffold
                   configuration can be deployed.

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

        request = cloud_deploy.GetTargetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_target,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
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

    async def create_target(
        self,
        request: Union[cloud_deploy.CreateTargetRequest, dict] = None,
        *,
        parent: str = None,
        target: cloud_deploy.Target = None,
        target_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Target in a given project and location.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_create_target():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.CreateTargetRequest(
                    parent="parent_value",
                    target_id="target_id_value",
                )

                # Make the request
                operation = client.create_target(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.CreateTargetRequest, dict]):
                The request object. The request object for
                `CreateTarget`.
            parent (:class:`str`):
                Required. The parent collection in which the ``Target``
                should be created. Format should be
                projects/{project_id}/locations/{location_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            target (:class:`google.cloud.deploy_v1.types.Target`):
                Required. The ``Target`` to create.
                This corresponds to the ``target`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            target_id (:class:`str`):
                Required. ID of the ``Target``.
                This corresponds to the ``target_id`` field
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
                :class:`google.cloud.deploy_v1.types.Target` A Target
                resource in the Google Cloud Deploy API.

                   A Target defines a location to which a Skaffold
                   configuration can be deployed.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, target, target_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_deploy.CreateTargetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if target is not None:
            request.target = target
        if target_id is not None:
            request.target_id = target_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_target,
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
            cloud_deploy.Target,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def update_target(
        self,
        request: Union[cloud_deploy.UpdateTargetRequest, dict] = None,
        *,
        target: cloud_deploy.Target = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the parameters of a single Target.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_update_target():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.UpdateTargetRequest(
                )

                # Make the request
                operation = client.update_target(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.UpdateTargetRequest, dict]):
                The request object. The request object for
                `UpdateTarget`.
            target (:class:`google.cloud.deploy_v1.types.Target`):
                Required. The ``Target`` to update.
                This corresponds to the ``target`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. Field mask is used to specify the fields to be
                overwritten in the Target resource by the update. The
                fields specified in the update_mask are relative to the
                resource, not the full request. A field will be
                overwritten if it is in the mask. If the user does not
                provide a mask then all fields will be overwritten.

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
                :class:`google.cloud.deploy_v1.types.Target` A Target
                resource in the Google Cloud Deploy API.

                   A Target defines a location to which a Skaffold
                   configuration can be deployed.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([target, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_deploy.UpdateTargetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if target is not None:
            request.target = target
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_target,
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("target.name", request.target.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            cloud_deploy.Target,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_target(
        self,
        request: Union[cloud_deploy.DeleteTargetRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a single Target.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_delete_target():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.DeleteTargetRequest(
                    name="name_value",
                )

                # Make the request
                operation = client.delete_target(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.DeleteTargetRequest, dict]):
                The request object. The request object for
                `DeleteTarget`.
            name (:class:`str`):
                Required. The name of the ``Target`` to delete. Format
                should be
                projects/{project_id}/locations/{location_name}/targets/{target_name}.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_deploy.DeleteTargetRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_target,
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
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_releases(
        self,
        request: Union[cloud_deploy.ListReleasesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListReleasesAsyncPager:
        r"""Lists Releases in a given project and location.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_list_releases():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ListReleasesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_releases(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ListReleasesRequest, dict]):
                The request object. The request object for
                `ListReleases`.
            parent (:class:`str`):
                Required. The ``DeliveryPipeline`` which owns this
                collection of ``Release`` objects.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.services.cloud_deploy.pagers.ListReleasesAsyncPager:
                The response object from ListReleases.

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

        request = cloud_deploy.ListReleasesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_releases,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
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
        response = pagers.ListReleasesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_release(
        self,
        request: Union[cloud_deploy.GetReleaseRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.Release:
        r"""Gets details of a single Release.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_get_release():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetReleaseRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_release(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetReleaseRequest, dict]):
                The request object. The request object for `GetRelease`.
            name (:class:`str`):
                Required. Name of the ``Release``. Format must be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.Release:
                A Release resource in the Google Cloud Deploy API.

                   A Release defines a specific Skaffold configuration
                   instance that can be deployed.

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

        request = cloud_deploy.GetReleaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_release,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
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

    async def create_release(
        self,
        request: Union[cloud_deploy.CreateReleaseRequest, dict] = None,
        *,
        parent: str = None,
        release: cloud_deploy.Release = None,
        release_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Release in a given project and
        location.


        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_create_release():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.CreateReleaseRequest(
                    parent="parent_value",
                    release_id="release_id_value",
                )

                # Make the request
                operation = client.create_release(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.CreateReleaseRequest, dict]):
                The request object. The request object for
                `CreateRelease`,
            parent (:class:`str`):
                Required. The parent collection in which the ``Release``
                should be created. Format should be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            release (:class:`google.cloud.deploy_v1.types.Release`):
                Required. The ``Release`` to create.
                This corresponds to the ``release`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            release_id (:class:`str`):
                Required. ID of the ``Release``.
                This corresponds to the ``release_id`` field
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
                :class:`google.cloud.deploy_v1.types.Release` A Release
                resource in the Google Cloud Deploy API.

                   A Release defines a specific Skaffold configuration
                   instance that can be deployed.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, release, release_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_deploy.CreateReleaseRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if release is not None:
            request.release = release
        if release_id is not None:
            request.release_id = release_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_release,
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
            cloud_deploy.Release,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def approve_rollout(
        self,
        request: Union[cloud_deploy.ApproveRolloutRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.ApproveRolloutResponse:
        r"""Approves a Rollout.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_approve_rollout():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ApproveRolloutRequest(
                    name="name_value",
                    approved=True,
                )

                # Make the request
                response = client.approve_rollout(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ApproveRolloutRequest, dict]):
                The request object. The request object used by
                `ApproveRollout`.
            name (:class:`str`):
                Required. Name of the Rollout. Format
                is
                projects/{project}/locations/{location}/deliveryPipelines/{deliveryPipeline}/
                releases/{release}/rollouts/{rollout}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.ApproveRolloutResponse:
                The response object from ApproveRollout.
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

        request = cloud_deploy.ApproveRolloutRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.approve_rollout,
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

    async def list_rollouts(
        self,
        request: Union[cloud_deploy.ListRolloutsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListRolloutsAsyncPager:
        r"""Lists Rollouts in a given project and location.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_list_rollouts():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.ListRolloutsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_rollouts(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.ListRolloutsRequest, dict]):
                The request object. ListRolloutsRequest is the request
                object used by `ListRollouts`.
            parent (:class:`str`):
                Required. The ``Release`` which owns this collection of
                ``Rollout`` objects.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.services.cloud_deploy.pagers.ListRolloutsAsyncPager:
                ListRolloutsResponse is the response object reutrned by
                ListRollouts.

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

        request = cloud_deploy.ListRolloutsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_rollouts,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
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
        response = pagers.ListRolloutsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_rollout(
        self,
        request: Union[cloud_deploy.GetRolloutRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.Rollout:
        r"""Gets details of a single Rollout.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_get_rollout():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetRolloutRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_rollout(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetRolloutRequest, dict]):
                The request object. GetRolloutRequest is the request
                object used by `GetRollout`.
            name (:class:`str`):
                Required. Name of the ``Rollout``. Format must be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}/rollouts/{rollout_name}.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.Rollout:
                A Rollout resource in the Google Cloud Deploy API.

                   A Rollout contains information around a specific
                   deployment to a Target.

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

        request = cloud_deploy.GetRolloutRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_rollout,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
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

    async def create_rollout(
        self,
        request: Union[cloud_deploy.CreateRolloutRequest, dict] = None,
        *,
        parent: str = None,
        rollout: cloud_deploy.Rollout = None,
        rollout_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new Rollout in a given project and
        location.


        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_create_rollout():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                rollout = deploy_v1.Rollout()
                rollout.target_id = "target_id_value"

                request = deploy_v1.CreateRolloutRequest(
                    parent="parent_value",
                    rollout_id="rollout_id_value",
                    rollout=rollout,
                )

                # Make the request
                operation = client.create_rollout(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.CreateRolloutRequest, dict]):
                The request object. CreateRolloutRequest is the request
                object used by `CreateRollout`.
            parent (:class:`str`):
                Required. The parent collection in which the ``Rollout``
                should be created. Format should be
                projects/{project_id}/locations/{location_name}/deliveryPipelines/{pipeline_name}/releases/{release_name}.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rollout (:class:`google.cloud.deploy_v1.types.Rollout`):
                Required. The ``Rollout`` to create.
                This corresponds to the ``rollout`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rollout_id (:class:`str`):
                Required. ID of the ``Rollout``.
                This corresponds to the ``rollout_id`` field
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
                :class:`google.cloud.deploy_v1.types.Rollout` A Rollout
                resource in the Google Cloud Deploy API.

                   A Rollout contains information around a specific
                   deployment to a Target.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, rollout, rollout_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = cloud_deploy.CreateRolloutRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if rollout is not None:
            request.rollout = rollout
        if rollout_id is not None:
            request.rollout_id = rollout_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_rollout,
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
            cloud_deploy.Rollout,
            metadata_type=cloud_deploy.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def get_config(
        self,
        request: Union[cloud_deploy.GetConfigRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> cloud_deploy.Config:
        r"""Gets the configuration for a location.

        .. code-block:: python

            from google.cloud import deploy_v1

            def sample_get_config():
                # Create a client
                client = deploy_v1.CloudDeployClient()

                # Initialize request argument(s)
                request = deploy_v1.GetConfigRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.deploy_v1.types.GetConfigRequest, dict]):
                The request object. Request to get a configuration.
            name (:class:`str`):
                Required. Name of requested
                configuration.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.deploy_v1.types.Config:
                Service-wide configuration.
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

        request = cloud_deploy.GetConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_config,
            default_retry=retries.Retry(
                initial=1.0,
                maximum=60.0,
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-deploy",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("CloudDeployAsyncClient",)
