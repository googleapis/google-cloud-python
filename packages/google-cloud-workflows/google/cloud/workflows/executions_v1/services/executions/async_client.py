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

from google.cloud.workflows.executions_v1.services.executions import pagers
from google.cloud.workflows.executions_v1.types import executions
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import ExecutionsTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ExecutionsGrpcAsyncIOTransport
from .client import ExecutionsClient


class ExecutionsAsyncClient:
    """Executions is used to start and manage running instances of
    [Workflows][google.cloud.workflows.v1.Workflow] called executions.
    """

    _client: ExecutionsClient

    DEFAULT_ENDPOINT = ExecutionsClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ExecutionsClient.DEFAULT_MTLS_ENDPOINT

    execution_path = staticmethod(ExecutionsClient.execution_path)
    parse_execution_path = staticmethod(ExecutionsClient.parse_execution_path)
    workflow_path = staticmethod(ExecutionsClient.workflow_path)
    parse_workflow_path = staticmethod(ExecutionsClient.parse_workflow_path)
    common_billing_account_path = staticmethod(
        ExecutionsClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ExecutionsClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ExecutionsClient.common_folder_path)
    parse_common_folder_path = staticmethod(ExecutionsClient.parse_common_folder_path)
    common_organization_path = staticmethod(ExecutionsClient.common_organization_path)
    parse_common_organization_path = staticmethod(
        ExecutionsClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ExecutionsClient.common_project_path)
    parse_common_project_path = staticmethod(ExecutionsClient.parse_common_project_path)
    common_location_path = staticmethod(ExecutionsClient.common_location_path)
    parse_common_location_path = staticmethod(
        ExecutionsClient.parse_common_location_path
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
            ExecutionsAsyncClient: The constructed client.
        """
        return ExecutionsClient.from_service_account_info.__func__(ExecutionsAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ExecutionsAsyncClient: The constructed client.
        """
        return ExecutionsClient.from_service_account_file.__func__(ExecutionsAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ExecutionsTransport:
        """Returns the transport used by the client instance.

        Returns:
            ExecutionsTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ExecutionsClient).get_transport_class, type(ExecutionsClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ExecutionsTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the executions client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ExecutionsTransport]): The
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
        self._client = ExecutionsClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_executions(
        self,
        request: executions.ListExecutionsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListExecutionsAsyncPager:
        r"""Returns a list of executions which belong to the
        workflow with the given name. The method returns
        executions of all workflow revisions. Returned
        executions are ordered by their start time (newest
        first).

        Args:
            request (:class:`google.cloud.workflows.executions_v1.types.ListExecutionsRequest`):
                The request object. Request for the
                [ListExecutions][]
                method.
            parent (:class:`str`):
                Required. Name of the workflow for
                which the executions should be listed.
                Format:
                projects/{project}/locations/{location}/workflows/{workflow}

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.workflows.executions_v1.services.executions.pagers.ListExecutionsAsyncPager:
                Response for the
                   [ListExecutions][google.cloud.workflows.executions.v1.Executions.ListExecutions]
                   method.

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

        request = executions.ListExecutionsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_executions,
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
        response = pagers.ListExecutionsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def create_execution(
        self,
        request: executions.CreateExecutionRequest = None,
        *,
        parent: str = None,
        execution: executions.Execution = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> executions.Execution:
        r"""Creates a new execution using the latest revision of
        the given workflow.

        Args:
            request (:class:`google.cloud.workflows.executions_v1.types.CreateExecutionRequest`):
                The request object. Request for the
                [CreateExecution][google.cloud.workflows.executions.v1.Executions.CreateExecution]
                method.
            parent (:class:`str`):
                Required. Name of the workflow for
                which an execution should be created.
                Format:
                projects/{project}/locations/{location}/workflows/{workflow}
                The latest revision of the workflow will
                be used.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            execution (:class:`google.cloud.workflows.executions_v1.types.Execution`):
                Required. Execution to be created.
                This corresponds to the ``execution`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.workflows.executions_v1.types.Execution:
                A running instance of a
                   [Workflow](/workflows/docs/reference/rest/v1/projects.locations.workflows).

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, execution])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = executions.CreateExecutionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if execution is not None:
            request.execution = execution

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_execution,
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

        # Done; return the response.
        return response

    async def get_execution(
        self,
        request: executions.GetExecutionRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> executions.Execution:
        r"""Returns an execution of the given name.

        Args:
            request (:class:`google.cloud.workflows.executions_v1.types.GetExecutionRequest`):
                The request object. Request for the
                [GetExecution][google.cloud.workflows.executions.v1.Executions.GetExecution]
                method.
            name (:class:`str`):
                Required. Name of the execution to be
                retrieved. Format:
                projects/{project}/locations/{location}/workflows/{workflow}/executions/{execution}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.workflows.executions_v1.types.Execution:
                A running instance of a
                   [Workflow](/workflows/docs/reference/rest/v1/projects.locations.workflows).

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

        request = executions.GetExecutionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_execution,
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

    async def cancel_execution(
        self,
        request: executions.CancelExecutionRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> executions.Execution:
        r"""Cancels an execution of the given name.

        Args:
            request (:class:`google.cloud.workflows.executions_v1.types.CancelExecutionRequest`):
                The request object. Request for the
                [CancelExecution][google.cloud.workflows.executions.v1.Executions.CancelExecution]
                method.
            name (:class:`str`):
                Required. Name of the execution to be
                cancelled. Format:
                projects/{project}/locations/{location}/workflows/{workflow}/executions/{execution}

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.workflows.executions_v1.types.Execution:
                A running instance of a
                   [Workflow](/workflows/docs/reference/rest/v1/projects.locations.workflows).

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

        request = executions.CancelExecutionRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.cancel_execution,
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


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-workflow",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ExecutionsAsyncClient",)
