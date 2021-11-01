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
from google.cloud.dataproc_v1.services.workflow_template_service import pagers
from google.cloud.dataproc_v1.types import workflow_templates
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import WorkflowTemplateServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import WorkflowTemplateServiceGrpcAsyncIOTransport
from .client import WorkflowTemplateServiceClient


class WorkflowTemplateServiceAsyncClient:
    """The API interface for managing Workflow Templates in the
    Dataproc API.
    """

    _client: WorkflowTemplateServiceClient

    DEFAULT_ENDPOINT = WorkflowTemplateServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = WorkflowTemplateServiceClient.DEFAULT_MTLS_ENDPOINT

    cluster_path = staticmethod(WorkflowTemplateServiceClient.cluster_path)
    parse_cluster_path = staticmethod(WorkflowTemplateServiceClient.parse_cluster_path)
    service_path = staticmethod(WorkflowTemplateServiceClient.service_path)
    parse_service_path = staticmethod(WorkflowTemplateServiceClient.parse_service_path)
    workflow_template_path = staticmethod(
        WorkflowTemplateServiceClient.workflow_template_path
    )
    parse_workflow_template_path = staticmethod(
        WorkflowTemplateServiceClient.parse_workflow_template_path
    )
    common_billing_account_path = staticmethod(
        WorkflowTemplateServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        WorkflowTemplateServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(WorkflowTemplateServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        WorkflowTemplateServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        WorkflowTemplateServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        WorkflowTemplateServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        WorkflowTemplateServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        WorkflowTemplateServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        WorkflowTemplateServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        WorkflowTemplateServiceClient.parse_common_location_path
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
            WorkflowTemplateServiceAsyncClient: The constructed client.
        """
        return WorkflowTemplateServiceClient.from_service_account_info.__func__(WorkflowTemplateServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            WorkflowTemplateServiceAsyncClient: The constructed client.
        """
        return WorkflowTemplateServiceClient.from_service_account_file.__func__(WorkflowTemplateServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> WorkflowTemplateServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            WorkflowTemplateServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(WorkflowTemplateServiceClient).get_transport_class,
        type(WorkflowTemplateServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, WorkflowTemplateServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the workflow template service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.WorkflowTemplateServiceTransport]): The
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
        self._client = WorkflowTemplateServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_workflow_template(
        self,
        request: Union[workflow_templates.CreateWorkflowTemplateRequest, dict] = None,
        *,
        parent: str = None,
        template: workflow_templates.WorkflowTemplate = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> workflow_templates.WorkflowTemplate:
        r"""Creates new workflow template.

        Args:
            request (Union[google.cloud.dataproc_v1.types.CreateWorkflowTemplateRequest, dict]):
                The request object. A request to create a workflow
                template.
            parent (:class:`str`):
                Required. The resource name of the region or location,
                as described in
                https://cloud.google.com/apis/design/resource_names.

                -  For ``projects.regions.workflowTemplates,create``,
                   the resource name of the region has the following
                   format: ``projects/{project_id}/regions/{region}``

                -  For ``projects.locations.workflowTemplates.create``,
                   the resource name of the location has the following
                   format:
                   ``projects/{project_id}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            template (:class:`google.cloud.dataproc_v1.types.WorkflowTemplate`):
                Required. The Dataproc workflow
                template to create.

                This corresponds to the ``template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataproc_v1.types.WorkflowTemplate:
                A Dataproc workflow template
                resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, template])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = workflow_templates.CreateWorkflowTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if template is not None:
            request.template = template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_workflow_template,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
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

    async def get_workflow_template(
        self,
        request: Union[workflow_templates.GetWorkflowTemplateRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> workflow_templates.WorkflowTemplate:
        r"""Retrieves the latest workflow template.
        Can retrieve previously instantiated template by
        specifying optional version parameter.

        Args:
            request (Union[google.cloud.dataproc_v1.types.GetWorkflowTemplateRequest, dict]):
                The request object. A request to fetch a workflow
                template.
            name (:class:`str`):
                Required. The resource name of the workflow template, as
                described in
                https://cloud.google.com/apis/design/resource_names.

                -  For ``projects.regions.workflowTemplates.get``, the
                   resource name of the template has the following
                   format:
                   ``projects/{project_id}/regions/{region}/workflowTemplates/{template_id}``

                -  For ``projects.locations.workflowTemplates.get``, the
                   resource name of the template has the following
                   format:
                   ``projects/{project_id}/locations/{location}/workflowTemplates/{template_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataproc_v1.types.WorkflowTemplate:
                A Dataproc workflow template
                resource.

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

        request = workflow_templates.GetWorkflowTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_workflow_template,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
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

        # Done; return the response.
        return response

    async def instantiate_workflow_template(
        self,
        request: Union[
            workflow_templates.InstantiateWorkflowTemplateRequest, dict
        ] = None,
        *,
        name: str = None,
        parameters: Sequence[
            workflow_templates.InstantiateWorkflowTemplateRequest.ParametersEntry
        ] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Instantiates a template and begins execution.

        The returned Operation can be used to track execution of
        workflow by polling
        [operations.get][google.longrunning.Operations.GetOperation].
        The Operation will complete when entire workflow is finished.

        The running workflow can be aborted via
        [operations.cancel][google.longrunning.Operations.CancelOperation].
        This will cause any inflight jobs to be cancelled and
        workflow-owned clusters to be deleted.

        The [Operation.metadata][google.longrunning.Operation.metadata]
        will be
        `WorkflowMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#workflowmetadata>`__.
        Also see `Using
        WorkflowMetadata <https://cloud.google.com/dataproc/docs/concepts/workflows/debugging#using_workflowmetadata>`__.

        On successful completion,
        [Operation.response][google.longrunning.Operation.response] will
        be [Empty][google.protobuf.Empty].

        Args:
            request (Union[google.cloud.dataproc_v1.types.InstantiateWorkflowTemplateRequest, dict]):
                The request object. A request to instantiate a workflow
                template.
            name (:class:`str`):
                Required. The resource name of the workflow template, as
                described in
                https://cloud.google.com/apis/design/resource_names.

                -  For
                   ``projects.regions.workflowTemplates.instantiate``,
                   the resource name of the template has the following
                   format:
                   ``projects/{project_id}/regions/{region}/workflowTemplates/{template_id}``

                -  For
                   ``projects.locations.workflowTemplates.instantiate``,
                   the resource name of the template has the following
                   format:
                   ``projects/{project_id}/locations/{location}/workflowTemplates/{template_id}``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            parameters (:class:`Sequence[google.cloud.dataproc_v1.types.InstantiateWorkflowTemplateRequest.ParametersEntry]`):
                Optional. Map from parameter names to
                values that should be used for those
                parameters. Values may not exceed 1000
                characters.

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
        has_flattened_params = any([name, parameters])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = workflow_templates.InstantiateWorkflowTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        if parameters:
            request.parameters.update(parameters)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.instantiate_workflow_template,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
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
            metadata_type=workflow_templates.WorkflowMetadata,
        )

        # Done; return the response.
        return response

    async def instantiate_inline_workflow_template(
        self,
        request: Union[
            workflow_templates.InstantiateInlineWorkflowTemplateRequest, dict
        ] = None,
        *,
        parent: str = None,
        template: workflow_templates.WorkflowTemplate = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Instantiates a template and begins execution.

        This method is equivalent to executing the sequence
        [CreateWorkflowTemplate][google.cloud.dataproc.v1.WorkflowTemplateService.CreateWorkflowTemplate],
        [InstantiateWorkflowTemplate][google.cloud.dataproc.v1.WorkflowTemplateService.InstantiateWorkflowTemplate],
        [DeleteWorkflowTemplate][google.cloud.dataproc.v1.WorkflowTemplateService.DeleteWorkflowTemplate].

        The returned Operation can be used to track execution of
        workflow by polling
        [operations.get][google.longrunning.Operations.GetOperation].
        The Operation will complete when entire workflow is finished.

        The running workflow can be aborted via
        [operations.cancel][google.longrunning.Operations.CancelOperation].
        This will cause any inflight jobs to be cancelled and
        workflow-owned clusters to be deleted.

        The [Operation.metadata][google.longrunning.Operation.metadata]
        will be
        `WorkflowMetadata <https://cloud.google.com/dataproc/docs/reference/rpc/google.cloud.dataproc.v1#workflowmetadata>`__.
        Also see `Using
        WorkflowMetadata <https://cloud.google.com/dataproc/docs/concepts/workflows/debugging#using_workflowmetadata>`__.

        On successful completion,
        [Operation.response][google.longrunning.Operation.response] will
        be [Empty][google.protobuf.Empty].

        Args:
            request (Union[google.cloud.dataproc_v1.types.InstantiateInlineWorkflowTemplateRequest, dict]):
                The request object. A request to instantiate an inline
                workflow template.
            parent (:class:`str`):
                Required. The resource name of the region or location,
                as described in
                https://cloud.google.com/apis/design/resource_names.

                -  For
                   ``projects.regions.workflowTemplates,instantiateinline``,
                   the resource name of the region has the following
                   format: ``projects/{project_id}/regions/{region}``

                -  For
                   ``projects.locations.workflowTemplates.instantiateinline``,
                   the resource name of the location has the following
                   format:
                   ``projects/{project_id}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            template (:class:`google.cloud.dataproc_v1.types.WorkflowTemplate`):
                Required. The workflow template to
                instantiate.

                This corresponds to the ``template`` field
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
        has_flattened_params = any([parent, template])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = workflow_templates.InstantiateInlineWorkflowTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if template is not None:
            request.template = template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.instantiate_inline_workflow_template,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
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
            empty_pb2.Empty,
            metadata_type=workflow_templates.WorkflowMetadata,
        )

        # Done; return the response.
        return response

    async def update_workflow_template(
        self,
        request: Union[workflow_templates.UpdateWorkflowTemplateRequest, dict] = None,
        *,
        template: workflow_templates.WorkflowTemplate = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> workflow_templates.WorkflowTemplate:
        r"""Updates (replaces) workflow template. The updated
        template must contain version that matches the current
        server version.

        Args:
            request (Union[google.cloud.dataproc_v1.types.UpdateWorkflowTemplateRequest, dict]):
                The request object. A request to update a workflow
                template.
            template (:class:`google.cloud.dataproc_v1.types.WorkflowTemplate`):
                Required. The updated workflow template.

                The ``template.version`` field must match the current
                version.

                This corresponds to the ``template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataproc_v1.types.WorkflowTemplate:
                A Dataproc workflow template
                resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([template])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = workflow_templates.UpdateWorkflowTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if template is not None:
            request.template = template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_workflow_template,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("template.name", request.template.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_workflow_templates(
        self,
        request: Union[workflow_templates.ListWorkflowTemplatesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListWorkflowTemplatesAsyncPager:
        r"""Lists workflows that match the specified filter in
        the request.

        Args:
            request (Union[google.cloud.dataproc_v1.types.ListWorkflowTemplatesRequest, dict]):
                The request object. A request to list workflow templates
                in a project.
            parent (:class:`str`):
                Required. The resource name of the region or location,
                as described in
                https://cloud.google.com/apis/design/resource_names.

                -  For ``projects.regions.workflowTemplates,list``, the
                   resource name of the region has the following format:
                   ``projects/{project_id}/regions/{region}``

                -  For ``projects.locations.workflowTemplates.list``,
                   the resource name of the location has the following
                   format:
                   ``projects/{project_id}/locations/{location}``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.dataproc_v1.services.workflow_template_service.pagers.ListWorkflowTemplatesAsyncPager:
                A response to a request to list
                workflow templates in a project.
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

        request = workflow_templates.ListWorkflowTemplatesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_workflow_templates,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
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
        response = pagers.ListWorkflowTemplatesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_workflow_template(
        self,
        request: Union[workflow_templates.DeleteWorkflowTemplateRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a workflow template. It does not cancel in-
        rogress workflows.

        Args:
            request (Union[google.cloud.dataproc_v1.types.DeleteWorkflowTemplateRequest, dict]):
                The request object. A request to delete a workflow
                template.
                Currently started workflows will remain running.
            name (:class:`str`):
                Required. The resource name of the workflow template, as
                described in
                https://cloud.google.com/apis/design/resource_names.

                -  For ``projects.regions.workflowTemplates.delete``,
                   the resource name of the template has the following
                   format:
                   ``projects/{project_id}/regions/{region}/workflowTemplates/{template_id}``

                -  For
                   ``projects.locations.workflowTemplates.instantiate``,
                   the resource name of the template has the following
                   format:
                   ``projects/{project_id}/locations/{location}/workflowTemplates/{template_id}``

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

        request = workflow_templates.DeleteWorkflowTemplateRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_workflow_template,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=600.0,
            ),
            default_timeout=600.0,
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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-dataproc",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("WorkflowTemplateServiceAsyncClient",)
