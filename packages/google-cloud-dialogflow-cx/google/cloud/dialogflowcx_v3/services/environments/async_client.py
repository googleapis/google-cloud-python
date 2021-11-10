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
from google.cloud.dialogflowcx_v3.services.environments import pagers
from google.cloud.dialogflowcx_v3.types import environment
from google.cloud.dialogflowcx_v3.types import environment as gcdc_environment
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import EnvironmentsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import EnvironmentsGrpcAsyncIOTransport
from .client import EnvironmentsClient


class EnvironmentsAsyncClient:
    """Service for managing
    [Environments][google.cloud.dialogflow.cx.v3.Environment].
    """

    _client: EnvironmentsClient

    DEFAULT_ENDPOINT = EnvironmentsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = EnvironmentsClient.DEFAULT_MTLS_ENDPOINT

    continuous_test_result_path = staticmethod(
        EnvironmentsClient.continuous_test_result_path
    )
    parse_continuous_test_result_path = staticmethod(
        EnvironmentsClient.parse_continuous_test_result_path
    )
    environment_path = staticmethod(EnvironmentsClient.environment_path)
    parse_environment_path = staticmethod(EnvironmentsClient.parse_environment_path)
    test_case_path = staticmethod(EnvironmentsClient.test_case_path)
    parse_test_case_path = staticmethod(EnvironmentsClient.parse_test_case_path)
    test_case_result_path = staticmethod(EnvironmentsClient.test_case_result_path)
    parse_test_case_result_path = staticmethod(
        EnvironmentsClient.parse_test_case_result_path
    )
    version_path = staticmethod(EnvironmentsClient.version_path)
    parse_version_path = staticmethod(EnvironmentsClient.parse_version_path)
    common_billing_account_path = staticmethod(
        EnvironmentsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        EnvironmentsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(EnvironmentsClient.common_folder_path)
    parse_common_folder_path = staticmethod(EnvironmentsClient.parse_common_folder_path)
    common_organization_path = staticmethod(EnvironmentsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        EnvironmentsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(EnvironmentsClient.common_project_path)
    parse_common_project_path = staticmethod(
        EnvironmentsClient.parse_common_project_path
    )
    common_location_path = staticmethod(EnvironmentsClient.common_location_path)
    parse_common_location_path = staticmethod(
        EnvironmentsClient.parse_common_location_path
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
            EnvironmentsAsyncClient: The constructed client.
        """
        return EnvironmentsClient.from_service_account_info.__func__(EnvironmentsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            EnvironmentsAsyncClient: The constructed client.
        """
        return EnvironmentsClient.from_service_account_file.__func__(EnvironmentsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> EnvironmentsTransport:
        """Returns the transport used by the client instance.

        Returns:
            EnvironmentsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(EnvironmentsClient).get_transport_class, type(EnvironmentsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, EnvironmentsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the environments client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.EnvironmentsTransport]): The
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
        self._client = EnvironmentsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_environments(
        self,
        request: Union[environment.ListEnvironmentsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEnvironmentsAsyncPager:
        r"""Returns the list of all environments in the specified
        [Agent][google.cloud.dialogflow.cx.v3.Agent].

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.ListEnvironmentsRequest, dict]):
                The request object. The request message for
                [Environments.ListEnvironments][google.cloud.dialogflow.cx.v3.Environments.ListEnvironments].
            parent (:class:`str`):
                Required. The
                [Agent][google.cloud.dialogflow.cx.v3.Agent] to list all
                environments for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.services.environments.pagers.ListEnvironmentsAsyncPager:
                The response message for
                [Environments.ListEnvironments][google.cloud.dialogflow.cx.v3.Environments.ListEnvironments].

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

        request = environment.ListEnvironmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_environments,
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
        response = pagers.ListEnvironmentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_environment(
        self,
        request: Union[environment.GetEnvironmentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> environment.Environment:
        r"""Retrieves the specified
        [Environment][google.cloud.dialogflow.cx.v3.Environment].

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.GetEnvironmentRequest, dict]):
                The request object. The request message for
                [Environments.GetEnvironment][google.cloud.dialogflow.cx.v3.Environments.GetEnvironment].
            name (:class:`str`):
                Required. The name of the
                [Environment][google.cloud.dialogflow.cx.v3.Environment].
                Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.types.Environment:
                Represents an environment for an
                agent. You can create multiple versions
                of your agent and publish them to
                separate environments. When you edit an
                agent, you are editing the draft agent.
                At any point, you can save the draft
                agent as an agent version, which is an
                immutable snapshot of your agent. When
                you save the draft agent, it is
                published to the default environment.
                When you create agent versions, you can
                publish them to custom environments. You
                can create a variety of custom
                environments for testing, development,
                production, etc.

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

        request = environment.GetEnvironmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_environment,
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

    async def create_environment(
        self,
        request: Union[gcdc_environment.CreateEnvironmentRequest, dict] = None,
        *,
        parent: str = None,
        environment: gcdc_environment.Environment = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates an
        [Environment][google.cloud.dialogflow.cx.v3.Environment] in the
        specified [Agent][google.cloud.dialogflow.cx.v3.Agent].

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``: An empty `Struct
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct>`__
        -  ``response``:
           [Environment][google.cloud.dialogflow.cx.v3.Environment]

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.CreateEnvironmentRequest, dict]):
                The request object. The request message for
                [Environments.CreateEnvironment][google.cloud.dialogflow.cx.v3.Environments.CreateEnvironment].
            parent (:class:`str`):
                Required. The
                [Agent][google.cloud.dialogflow.cx.v3.Agent] to create
                an
                [Environment][google.cloud.dialogflow.cx.v3.Environment]
                for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            environment (:class:`google.cloud.dialogflowcx_v3.types.Environment`):
                Required. The environment to create.
                This corresponds to the ``environment`` field
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

                The result type for the operation will be :class:`google.cloud.dialogflowcx_v3.types.Environment` Represents an environment for an agent. You can create multiple versions
                   of your agent and publish them to separate
                   environments. When you edit an agent, you are editing
                   the draft agent. At any point, you can save the draft
                   agent as an agent version, which is an immutable
                   snapshot of your agent. When you save the draft
                   agent, it is published to the default environment.
                   When you create agent versions, you can publish them
                   to custom environments. You can create a variety of
                   custom environments for testing, development,
                   production, etc.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, environment])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_environment.CreateEnvironmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if environment is not None:
            request.environment = environment

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_environment,
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

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcdc_environment.Environment,
            metadata_type=struct_pb2.Struct,
        )

        # Done; return the response.
        return response

    async def update_environment(
        self,
        request: Union[gcdc_environment.UpdateEnvironmentRequest, dict] = None,
        *,
        environment: gcdc_environment.Environment = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Updates the specified
        [Environment][google.cloud.dialogflow.cx.v3.Environment].

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``: An empty `Struct
           message <https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct>`__
        -  ``response``:
           [Environment][google.cloud.dialogflow.cx.v3.Environment]

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.UpdateEnvironmentRequest, dict]):
                The request object. The request message for
                [Environments.UpdateEnvironment][google.cloud.dialogflow.cx.v3.Environments.UpdateEnvironment].
            environment (:class:`google.cloud.dialogflowcx_v3.types.Environment`):
                Required. The environment to update.
                This corresponds to the ``environment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
                Required. The mask to control which
                fields get updated.

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

                The result type for the operation will be :class:`google.cloud.dialogflowcx_v3.types.Environment` Represents an environment for an agent. You can create multiple versions
                   of your agent and publish them to separate
                   environments. When you edit an agent, you are editing
                   the draft agent. At any point, you can save the draft
                   agent as an agent version, which is an immutable
                   snapshot of your agent. When you save the draft
                   agent, it is published to the default environment.
                   When you create agent versions, you can publish them
                   to custom environments. You can create a variety of
                   custom environments for testing, development,
                   production, etc.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([environment, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcdc_environment.UpdateEnvironmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if environment is not None:
            request.environment = environment
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_environment,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("environment.name", request.environment.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            gcdc_environment.Environment,
            metadata_type=struct_pb2.Struct,
        )

        # Done; return the response.
        return response

    async def delete_environment(
        self,
        request: Union[environment.DeleteEnvironmentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified
        [Environment][google.cloud.dialogflow.cx.v3.Environment].

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.DeleteEnvironmentRequest, dict]):
                The request object. The request message for
                [Environments.DeleteEnvironment][google.cloud.dialogflow.cx.v3.Environments.DeleteEnvironment].
            name (:class:`str`):
                Required. The name of the
                [Environment][google.cloud.dialogflow.cx.v3.Environment]
                to delete. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>``.

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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = environment.DeleteEnvironmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_environment,
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
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def lookup_environment_history(
        self,
        request: Union[environment.LookupEnvironmentHistoryRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.LookupEnvironmentHistoryAsyncPager:
        r"""Looks up the history of the specified
        [Environment][google.cloud.dialogflow.cx.v3.Environment].

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.LookupEnvironmentHistoryRequest, dict]):
                The request object. The request message for
                [Environments.LookupEnvironmentHistory][google.cloud.dialogflow.cx.v3.Environments.LookupEnvironmentHistory].
            name (:class:`str`):
                Required. Resource name of the environment to look up
                the history for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.services.environments.pagers.LookupEnvironmentHistoryAsyncPager:
                The response message for
                [Environments.LookupEnvironmentHistory][google.cloud.dialogflow.cx.v3.Environments.LookupEnvironmentHistory].

                Iterating over this object will yield results and
                resolve additional pages automatically.

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

        request = environment.LookupEnvironmentHistoryRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.lookup_environment_history,
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

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.LookupEnvironmentHistoryAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def run_continuous_test(
        self,
        request: Union[environment.RunContinuousTestRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Kicks off a continuous test under the specified
        [Environment][google.cloud.dialogflow.cx.v3.Environment].

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [RunContinuousTestMetadata][google.cloud.dialogflow.cx.v3.RunContinuousTestMetadata]
        -  ``response``:
           [RunContinuousTestResponse][google.cloud.dialogflow.cx.v3.RunContinuousTestResponse]

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.RunContinuousTestRequest, dict]):
                The request object. The request message for
                [Environments.RunContinuousTest][google.cloud.dialogflow.cx.v3.Environments.RunContinuousTest].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflowcx_v3.types.RunContinuousTestResponse`
                The response message for
                [Environments.RunContinuousTest][google.cloud.dialogflow.cx.v3.Environments.RunContinuousTest].

        """
        # Create or coerce a protobuf request object.
        request = environment.RunContinuousTestRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.run_continuous_test,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("environment", request.environment),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            environment.RunContinuousTestResponse,
            metadata_type=environment.RunContinuousTestMetadata,
        )

        # Done; return the response.
        return response

    async def list_continuous_test_results(
        self,
        request: Union[environment.ListContinuousTestResultsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListContinuousTestResultsAsyncPager:
        r"""Fetches a list of continuous test results for a given
        environment.

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.ListContinuousTestResultsRequest, dict]):
                The request object. The request message for
                [Environments.ListContinuousTestResults][google.cloud.dialogflow.cx.v3.Environments.ListContinuousTestResults].
            parent (:class:`str`):
                Required. The environment to list results for. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/ environments/<Environment ID>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dialogflowcx_v3.services.environments.pagers.ListContinuousTestResultsAsyncPager:
                The response message for
                [Environments.ListTestCaseResults][].

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

        request = environment.ListContinuousTestResultsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_continuous_test_results,
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
        response = pagers.ListContinuousTestResultsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def deploy_flow(
        self,
        request: Union[environment.DeployFlowRequest, dict] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deploys a flow to the specified
        [Environment][google.cloud.dialogflow.cx.v3.Environment].

        This method is a `long-running
        operation <https://cloud.google.com/dialogflow/cx/docs/how/long-running-operation>`__.
        The returned ``Operation`` type has the following
        method-specific fields:

        -  ``metadata``:
           [DeployFlowMetadata][google.cloud.dialogflow.cx.v3.DeployFlowMetadata]
        -  ``response``:
           [DeployFlowResponse][google.cloud.dialogflow.cx.v3.DeployFlowResponse]

        Args:
            request (Union[google.cloud.dialogflowcx_v3.types.DeployFlowRequest, dict]):
                The request object. The request message for
                [Environments.DeployFlow][google.cloud.dialogflow.cx.v3.Environments.DeployFlow].
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.dialogflowcx_v3.types.DeployFlowResponse`
                The response message for
                [Environments.DeployFlow][google.cloud.dialogflow.cx.v3.Environments.DeployFlow].

        """
        # Create or coerce a protobuf request object.
        request = environment.DeployFlowRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.deploy_flow,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("environment", request.environment),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            environment.DeployFlowResponse,
            metadata_type=environment.DeployFlowMetadata,
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
            "google-cloud-dialogflowcx",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("EnvironmentsAsyncClient",)
