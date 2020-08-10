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
import os
import re
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation
from google.api_core import operation_async
from google.cloud.dataproc_v1.services.workflow_template_service import pagers
from google.cloud.dataproc_v1.types import workflow_templates
from google.protobuf import empty_pb2 as empty  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import WorkflowTemplateServiceTransport
from .transports.grpc import WorkflowTemplateServiceGrpcTransport
from .transports.grpc_asyncio import WorkflowTemplateServiceGrpcAsyncIOTransport


class WorkflowTemplateServiceClientMeta(type):
    """Metaclass for the WorkflowTemplateService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[WorkflowTemplateServiceTransport]]
    _transport_registry["grpc"] = WorkflowTemplateServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = WorkflowTemplateServiceGrpcAsyncIOTransport

    def get_transport_class(
        cls, label: str = None,
    ) -> Type[WorkflowTemplateServiceTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class WorkflowTemplateServiceClient(metaclass=WorkflowTemplateServiceClientMeta):
    """The API interface for managing Workflow Templates in the
    Dataproc API.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "dataproc.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

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
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def workflow_template_path(
        project: str, region: str, workflow_template: str,
    ) -> str:
        """Return a fully-qualified workflow_template string."""
        return "projects/{project}/regions/{region}/workflowTemplates/{workflow_template}".format(
            project=project, region=region, workflow_template=workflow_template,
        )

    @staticmethod
    def parse_workflow_template_path(path: str) -> Dict[str, str]:
        """Parse a workflow_template path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/regions/(?P<region>.+?)/workflowTemplates/(?P<workflow_template>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, WorkflowTemplateServiceTransport] = None,
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the workflow template service client.

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
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)
        if client_options is None:
            client_options = ClientOptions.ClientOptions()

        if client_options.api_endpoint is None:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS", "never")
            if use_mtls_env == "never":
                client_options.api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                client_options.api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                has_client_cert_source = (
                    client_options.client_cert_source is not None
                    or mtls.has_default_client_cert_source()
                )
                client_options.api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT
                    if has_client_cert_source
                    else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, WorkflowTemplateServiceTransport):
            # transport is a WorkflowTemplateServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=client_options.api_endpoint,
                scopes=client_options.scopes,
                api_mtls_endpoint=client_options.api_endpoint,
                client_cert_source=client_options.client_cert_source,
                quota_project_id=client_options.quota_project_id,
            )

    def create_workflow_template(
        self,
        request: workflow_templates.CreateWorkflowTemplateRequest = None,
        *,
        parent: str = None,
        template: workflow_templates.WorkflowTemplate = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> workflow_templates.WorkflowTemplate:
        r"""Creates new workflow template.

        Args:
            request (:class:`~.workflow_templates.CreateWorkflowTemplateRequest`):
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
            template (:class:`~.workflow_templates.WorkflowTemplate`):
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
            ~.workflow_templates.WorkflowTemplate:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a workflow_templates.CreateWorkflowTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, workflow_templates.CreateWorkflowTemplateRequest):
            request = workflow_templates.CreateWorkflowTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if template is not None:
                request.template = template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_workflow_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_workflow_template(
        self,
        request: workflow_templates.GetWorkflowTemplateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> workflow_templates.WorkflowTemplate:
        r"""Retrieves the latest workflow template.
        Can retrieve previously instantiated template by
        specifying optional version parameter.

        Args:
            request (:class:`~.workflow_templates.GetWorkflowTemplateRequest`):
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
            ~.workflow_templates.WorkflowTemplate:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a workflow_templates.GetWorkflowTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, workflow_templates.GetWorkflowTemplateRequest):
            request = workflow_templates.GetWorkflowTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_workflow_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def instantiate_workflow_template(
        self,
        request: workflow_templates.InstantiateWorkflowTemplateRequest = None,
        *,
        name: str = None,
        parameters: Sequence[
            workflow_templates.InstantiateWorkflowTemplateRequest.ParametersEntry
        ] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
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
            request (:class:`~.workflow_templates.InstantiateWorkflowTemplateRequest`):
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
            parameters (:class:`Sequence[~.workflow_templates.InstantiateWorkflowTemplateRequest.ParametersEntry]`):
                Optional. Map from parameter names to
                values that should be used for those
                parameters. Values may not exceed 100
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
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a workflow_templates.InstantiateWorkflowTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, workflow_templates.InstantiateWorkflowTemplateRequest
        ):
            request = workflow_templates.InstantiateWorkflowTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name
            if parameters is not None:
                request.parameters = parameters

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.instantiate_workflow_template
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty.Empty,
            metadata_type=workflow_templates.WorkflowMetadata,
        )

        # Done; return the response.
        return response

    def instantiate_inline_workflow_template(
        self,
        request: workflow_templates.InstantiateInlineWorkflowTemplateRequest = None,
        *,
        parent: str = None,
        template: workflow_templates.WorkflowTemplate = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
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
            request (:class:`~.workflow_templates.InstantiateInlineWorkflowTemplateRequest`):
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
            template (:class:`~.workflow_templates.WorkflowTemplate`):
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
            ~.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:``~.empty.Empty``: A generic empty message that
                you can re-use to avoid defining duplicated empty
                messages in your APIs. A typical example is to use it as
                the request or the response type of an API method. For
                instance:

                ::

                    service Foo {
                      rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);
                    }

                The JSON representation for ``Empty`` is empty JSON
                object ``{}``.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a workflow_templates.InstantiateInlineWorkflowTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, workflow_templates.InstantiateInlineWorkflowTemplateRequest
        ):
            request = workflow_templates.InstantiateInlineWorkflowTemplateRequest(
                request
            )

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if template is not None:
                request.template = template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.instantiate_inline_workflow_template
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty.Empty,
            metadata_type=workflow_templates.WorkflowMetadata,
        )

        # Done; return the response.
        return response

    def update_workflow_template(
        self,
        request: workflow_templates.UpdateWorkflowTemplateRequest = None,
        *,
        template: workflow_templates.WorkflowTemplate = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> workflow_templates.WorkflowTemplate:
        r"""Updates (replaces) workflow template. The updated
        template must contain version that matches the current
        server version.

        Args:
            request (:class:`~.workflow_templates.UpdateWorkflowTemplateRequest`):
                The request object. A request to update a workflow
                template.
            template (:class:`~.workflow_templates.WorkflowTemplate`):
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
            ~.workflow_templates.WorkflowTemplate:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a workflow_templates.UpdateWorkflowTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, workflow_templates.UpdateWorkflowTemplateRequest):
            request = workflow_templates.UpdateWorkflowTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if template is not None:
                request.template = template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_workflow_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("template.name", request.template.name),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_workflow_templates(
        self,
        request: workflow_templates.ListWorkflowTemplatesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListWorkflowTemplatesPager:
        r"""Lists workflows that match the specified filter in
        the request.

        Args:
            request (:class:`~.workflow_templates.ListWorkflowTemplatesRequest`):
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
            ~.pagers.ListWorkflowTemplatesPager:
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

        # Minor optimization to avoid making a copy if the user passes
        # in a workflow_templates.ListWorkflowTemplatesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, workflow_templates.ListWorkflowTemplatesRequest):
            request = workflow_templates.ListWorkflowTemplatesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_workflow_templates]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListWorkflowTemplatesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_workflow_template(
        self,
        request: workflow_templates.DeleteWorkflowTemplateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a workflow template. It does not cancel in-
        rogress workflows.

        Args:
            request (:class:`~.workflow_templates.DeleteWorkflowTemplateRequest`):
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

        # Minor optimization to avoid making a copy if the user passes
        # in a workflow_templates.DeleteWorkflowTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, workflow_templates.DeleteWorkflowTemplateRequest):
            request = workflow_templates.DeleteWorkflowTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_workflow_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-dataproc",).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("WorkflowTemplateServiceClient",)
