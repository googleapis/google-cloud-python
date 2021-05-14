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
from distutils import util
import os
import re
from typing import Callable, Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.notebooks_v1beta1.services.notebook_service import pagers
from google.cloud.notebooks_v1beta1.types import environment
from google.cloud.notebooks_v1beta1.types import instance
from google.cloud.notebooks_v1beta1.types import service
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import NotebookServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import NotebookServiceGrpcTransport
from .transports.grpc_asyncio import NotebookServiceGrpcAsyncIOTransport


class NotebookServiceClientMeta(type):
    """Metaclass for the NotebookService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[NotebookServiceTransport]]
    _transport_registry["grpc"] = NotebookServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = NotebookServiceGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[NotebookServiceTransport]:
        """Returns an appropriate transport class.

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


class NotebookServiceClient(metaclass=NotebookServiceClientMeta):
    """API v1beta1 service for Cloud AI Platform Notebooks."""

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

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

    DEFAULT_ENDPOINT = "notebooks.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
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
            NotebookServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

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
            NotebookServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> NotebookServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            NotebookServiceTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def environment_path(project: str, environment: str,) -> str:
        """Returns a fully-qualified environment string."""
        return "projects/{project}/environments/{environment}".format(
            project=project, environment=environment,
        )

    @staticmethod
    def parse_environment_path(path: str) -> Dict[str, str]:
        """Parses a environment path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/environments/(?P<environment>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def instance_path(project: str, instance: str,) -> str:
        """Returns a fully-qualified instance string."""
        return "projects/{project}/instances/{instance}".format(
            project=project, instance=instance,
        )

    @staticmethod
    def parse_instance_path(path: str) -> Dict[str, str]:
        """Parses a instance path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(billing_account: str,) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(folder: str,) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(folder=folder,)

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(organization: str,) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(organization=organization,)

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(project: str, location: str,) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project, location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, NotebookServiceTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the notebook service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, NotebookServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
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
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()

        # Create SSL credentials for mutual TLS if needed.
        use_client_cert = bool(
            util.strtobool(os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false"))
        )

        client_cert_source_func = None
        is_mtls = False
        if use_client_cert:
            if client_options.client_cert_source:
                is_mtls = True
                client_cert_source_func = client_options.client_cert_source
            else:
                is_mtls = mtls.has_default_client_cert_source()
                if is_mtls:
                    client_cert_source_func = mtls.default_client_cert_source()
                else:
                    client_cert_source_func = None

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        else:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
            if use_mtls_env == "never":
                api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                if is_mtls:
                    api_endpoint = self.DEFAULT_MTLS_ENDPOINT
                else:
                    api_endpoint = self.DEFAULT_ENDPOINT
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS_ENDPOINT value. Accepted "
                    "values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, NotebookServiceTransport):
            # transport is a NotebookServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
            )

    def list_instances(
        self,
        request: service.ListInstancesRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInstancesPager:
        r"""Lists instances in a given project and location.

        Args:
            request (google.cloud.notebooks_v1beta1.types.ListInstancesRequest):
                The request object. Request for listing notebook
                instances.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.notebooks_v1beta1.services.notebook_service.pagers.ListInstancesPager:
                Response for listing notebook
                instances.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListInstancesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListInstancesRequest):
            request = service.ListInstancesRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_instances]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListInstancesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_instance(
        self,
        request: service.GetInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> instance.Instance:
        r"""Gets details of a single Instance.

        Args:
            request (google.cloud.notebooks_v1beta1.types.GetInstanceRequest):
                The request object. Request for getting a notebook
                instance.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.notebooks_v1beta1.types.Instance:
                The definition of a notebook
                instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.GetInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetInstanceRequest):
            request = service.GetInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_instance]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_instance(
        self,
        request: service.CreateInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new Instance in a given project and
        location.

        Args:
            request (google.cloud.notebooks_v1beta1.types.CreateInstanceRequest):
                The request object. Request for creating a notebook
                instance.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.CreateInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.CreateInstanceRequest):
            request = service.CreateInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_instance]

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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def register_instance(
        self,
        request: service.RegisterInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Registers an existing legacy notebook instance to the
        Notebooks API server. Legacy instances are instances
        created with the legacy Compute Engine calls. They are
        not manageable by the Notebooks API out of the box. This
        call makes these instances manageable by the Notebooks
        API.

        Args:
            request (google.cloud.notebooks_v1beta1.types.RegisterInstanceRequest):
                The request object. Request for registering a notebook
                instance.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.RegisterInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.RegisterInstanceRequest):
            request = service.RegisterInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.register_instance]

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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def set_instance_accelerator(
        self,
        request: service.SetInstanceAcceleratorRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the guest accelerators of a single Instance.

        Args:
            request (google.cloud.notebooks_v1beta1.types.SetInstanceAcceleratorRequest):
                The request object. Request for setting instance
                accelerator.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.SetInstanceAcceleratorRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.SetInstanceAcceleratorRequest):
            request = service.SetInstanceAcceleratorRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_instance_accelerator]

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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def set_instance_machine_type(
        self,
        request: service.SetInstanceMachineTypeRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the machine type of a single Instance.

        Args:
            request (google.cloud.notebooks_v1beta1.types.SetInstanceMachineTypeRequest):
                The request object. Request for setting instance machine
                type.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.SetInstanceMachineTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.SetInstanceMachineTypeRequest):
            request = service.SetInstanceMachineTypeRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.set_instance_machine_type
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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def set_instance_labels(
        self,
        request: service.SetInstanceLabelsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the labels of an Instance.

        Args:
            request (google.cloud.notebooks_v1beta1.types.SetInstanceLabelsRequest):
                The request object. Request for setting instance labels.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.SetInstanceLabelsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.SetInstanceLabelsRequest):
            request = service.SetInstanceLabelsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_instance_labels]

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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_instance(
        self,
        request: service.DeleteInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single Instance.

        Args:
            request (google.cloud.notebooks_v1beta1.types.DeleteInstanceRequest):
                The request object. Request for deleting a notebook
                instance.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
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
        # Minor optimization to avoid making a copy if the user passes
        # in a service.DeleteInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.DeleteInstanceRequest):
            request = service.DeleteInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_instance]

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
            empty_pb2.Empty,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def start_instance(
        self,
        request: service.StartInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Starts a notebook instance.

        Args:
            request (google.cloud.notebooks_v1beta1.types.StartInstanceRequest):
                The request object. Request for starting a notebook
                instance
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.StartInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.StartInstanceRequest):
            request = service.StartInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.start_instance]

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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def stop_instance(
        self,
        request: service.StopInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Stops a notebook instance.

        Args:
            request (google.cloud.notebooks_v1beta1.types.StopInstanceRequest):
                The request object. Request for stopping a notebook
                instance
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.StopInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.StopInstanceRequest):
            request = service.StopInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.stop_instance]

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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def reset_instance(
        self,
        request: service.ResetInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Resets a notebook instance.

        Args:
            request (google.cloud.notebooks_v1beta1.types.ResetInstanceRequest):
                The request object. Request for reseting a notebook
                instance
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.ResetInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ResetInstanceRequest):
            request = service.ResetInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reset_instance]

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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def report_instance_info(
        self,
        request: service.ReportInstanceInfoRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Allows notebook instances to
        report their latest instance information to the
        Notebooks API server. The server will merge the reported
        information to the instance metadata store. Do not use
        this method directly.

        Args:
            request (google.cloud.notebooks_v1beta1.types.ReportInstanceInfoRequest):
                The request object. Request for notebook instances to
                report information to Notebooks API.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.ReportInstanceInfoRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ReportInstanceInfoRequest):
            request = service.ReportInstanceInfoRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.report_instance_info]

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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def is_instance_upgradeable(
        self,
        request: service.IsInstanceUpgradeableRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.IsInstanceUpgradeableResponse:
        r"""Check if a notebook instance is upgradable.

        Args:
            request (google.cloud.notebooks_v1beta1.types.IsInstanceUpgradeableRequest):
                The request object. Request for checking if a notebook
                instance is upgradeable.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.notebooks_v1beta1.types.IsInstanceUpgradeableResponse:
                Response for checking if a notebook
                instance is upgradeable.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.IsInstanceUpgradeableRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.IsInstanceUpgradeableRequest):
            request = service.IsInstanceUpgradeableRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.is_instance_upgradeable]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("notebook_instance", request.notebook_instance),)
            ),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def upgrade_instance(
        self,
        request: service.UpgradeInstanceRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Upgrades a notebook instance to the latest version.

        Args:
            request (google.cloud.notebooks_v1beta1.types.UpgradeInstanceRequest):
                The request object. Request for upgrading a notebook
                instance
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.UpgradeInstanceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.UpgradeInstanceRequest):
            request = service.UpgradeInstanceRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.upgrade_instance]

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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def upgrade_instance_internal(
        self,
        request: service.UpgradeInstanceInternalRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Allows notebook instances to
        call this endpoint to upgrade themselves. Do not use
        this method directly.

        Args:
            request (google.cloud.notebooks_v1beta1.types.UpgradeInstanceInternalRequest):
                The request object. Request for upgrading a notebook
                instance from within the VM
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.notebooks_v1beta1.types.Instance`
                The definition of a notebook instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.UpgradeInstanceInternalRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.UpgradeInstanceInternalRequest):
            request = service.UpgradeInstanceInternalRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.upgrade_instance_internal
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
            instance.Instance,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_environments(
        self,
        request: service.ListEnvironmentsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEnvironmentsPager:
        r"""Lists environments in a project.

        Args:
            request (google.cloud.notebooks_v1beta1.types.ListEnvironmentsRequest):
                The request object. Request for listing environments.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.notebooks_v1beta1.services.notebook_service.pagers.ListEnvironmentsPager:
                Response for listing environments.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.ListEnvironmentsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.ListEnvironmentsRequest):
            request = service.ListEnvironmentsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_environments]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListEnvironmentsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_environment(
        self,
        request: service.GetEnvironmentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> environment.Environment:
        r"""Gets details of a single Environment.

        Args:
            request (google.cloud.notebooks_v1beta1.types.GetEnvironmentRequest):
                The request object. Request for getting a notebook
                environment.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.notebooks_v1beta1.types.Environment:
                Definition of a software environment
                that is used to start a notebook
                instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.GetEnvironmentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.GetEnvironmentRequest):
            request = service.GetEnvironmentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_environment]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_environment(
        self,
        request: service.CreateEnvironmentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new Environment.

        Args:
            request (google.cloud.notebooks_v1beta1.types.CreateEnvironmentRequest):
                The request object. Request for creating a notebook
                environment.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.notebooks_v1beta1.types.Environment` Definition of a software environment that is used to start a notebook
                   instance.

        """
        # Create or coerce a protobuf request object.
        # Minor optimization to avoid making a copy if the user passes
        # in a service.CreateEnvironmentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.CreateEnvironmentRequest):
            request = service.CreateEnvironmentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_environment]

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
            environment.Environment,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_environment(
        self,
        request: service.DeleteEnvironmentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a single Environment.

        Args:
            request (google.cloud.notebooks_v1beta1.types.DeleteEnvironmentRequest):
                The request object. Request for deleting a notebook
                environment.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
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
        # Minor optimization to avoid making a copy if the user passes
        # in a service.DeleteEnvironmentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, service.DeleteEnvironmentRequest):
            request = service.DeleteEnvironmentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_environment]

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
            empty_pb2.Empty,
            metadata_type=service.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-notebooks",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("NotebookServiceClient",)
