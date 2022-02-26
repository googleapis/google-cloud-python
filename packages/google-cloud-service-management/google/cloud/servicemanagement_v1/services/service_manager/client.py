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
import os
import re
from typing import Dict, Optional, Sequence, Tuple, Type, Union
import pkg_resources

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api import auth_pb2  # type: ignore
from google.api import backend_pb2  # type: ignore
from google.api import billing_pb2  # type: ignore
from google.api import context_pb2  # type: ignore
from google.api import control_pb2  # type: ignore
from google.api import documentation_pb2  # type: ignore
from google.api import endpoint_pb2  # type: ignore
from google.api import http_pb2  # type: ignore
from google.api import log_pb2  # type: ignore
from google.api import logging_pb2  # type: ignore
from google.api import metric_pb2  # type: ignore
from google.api import monitored_resource_pb2  # type: ignore
from google.api import monitoring_pb2  # type: ignore
from google.api import quota_pb2  # type: ignore
from google.api import service_pb2  # type: ignore
from google.api import source_info_pb2  # type: ignore
from google.api import system_parameter_pb2  # type: ignore
from google.api import usage_pb2  # type: ignore
from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.servicemanagement_v1.services.service_manager import pagers
from google.cloud.servicemanagement_v1.types import resources
from google.cloud.servicemanagement_v1.types import servicemanager
from google.protobuf import any_pb2  # type: ignore
from google.protobuf import api_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import type_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from .transports.base import ServiceManagerTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import ServiceManagerGrpcTransport
from .transports.grpc_asyncio import ServiceManagerGrpcAsyncIOTransport


class ServiceManagerClientMeta(type):
    """Metaclass for the ServiceManager client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ServiceManagerTransport]]
    _transport_registry["grpc"] = ServiceManagerGrpcTransport
    _transport_registry["grpc_asyncio"] = ServiceManagerGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[ServiceManagerTransport]:
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


class ServiceManagerClient(metaclass=ServiceManagerClientMeta):
    """`Google Service Management API </service-management/overview>`__"""

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

    DEFAULT_ENDPOINT = "servicemanagement.googleapis.com"
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
            ServiceManagerClient: The constructed client.
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
            ServiceManagerClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ServiceManagerTransport:
        """Returns the transport used by the client instance.

        Returns:
            ServiceManagerTransport: The transport used by the client
                instance.
        """
        return self._transport

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

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
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
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Union[str, ServiceManagerTransport, None] = None,
        client_options: Optional[client_options_lib.ClientOptions] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the service manager client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ServiceManagerTransport]): The
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

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ServiceManagerTransport):
            # transport is a ServiceManagerTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
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
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
            )

    def list_services(
        self,
        request: Union[servicemanager.ListServicesRequest, dict] = None,
        *,
        producer_project_id: str = None,
        consumer_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServicesPager:
        r"""Lists managed services.
        Returns all public services. For authenticated users,
        also returns all services the calling user has
        "servicemanagement.services.get" permission for.


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_list_services():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.ListServicesRequest(
                )

                # Make the request
                page_result = client.list_services(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.ListServicesRequest, dict]):
                The request object. Request message for `ListServices`
                method.
            producer_project_id (str):
                Include services produced by the
                specified project.

                This corresponds to the ``producer_project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            consumer_id (str):
                Include services consumed by the specified consumer.

                The Google Service Management implementation accepts the
                following forms:

                -  project:<project_id>

                This corresponds to the ``consumer_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.servicemanagement_v1.services.service_manager.pagers.ListServicesPager:
                Response message for ListServices method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([producer_project_id, consumer_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.ListServicesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.ListServicesRequest):
            request = servicemanager.ListServicesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if producer_project_id is not None:
                request.producer_project_id = producer_project_id
            if consumer_id is not None:
                request.consumer_id = consumer_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_services]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListServicesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_service(
        self,
        request: Union[servicemanager.GetServiceRequest, dict] = None,
        *,
        service_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.ManagedService:
        r"""Gets a managed service. Authentication is required
        unless the service is public.


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_get_service():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.GetServiceRequest(
                    service_name="service_name_value",
                )

                # Make the request
                response = client.get_service(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.GetServiceRequest, dict]):
                The request object. Request message for `GetService`
                method.
            service_name (str):
                Required. The name of the service. See the
                ``ServiceManager`` overview for naming requirements. For
                example: ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.servicemanagement_v1.types.ManagedService:
                The full representation of a Service
                that is managed by Google Service
                Management.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.GetServiceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.GetServiceRequest):
            request = servicemanager.GetServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_name is not None:
                request.service_name = service_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_service]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_service(
        self,
        request: Union[servicemanager.CreateServiceRequest, dict] = None,
        *,
        service: resources.ManagedService = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new managed service.
        A managed service is immutable, and is subject to
        mandatory 30-day data retention. You cannot move a
        service or recreate it within 30 days after deletion.

        One producer project can own no more than 500 services.
        For security and reliability purposes, a production
        service should be hosted in a dedicated producer
        project.

        Operation<response: ManagedService>


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_create_service():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.CreateServiceRequest(
                )

                # Make the request
                operation = client.create_service(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.CreateServiceRequest, dict]):
                The request object. Request message for CreateService
                method.
            service (google.cloud.servicemanagement_v1.types.ManagedService):
                Required. Initial values for the
                service resource.

                This corresponds to the ``service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.servicemanagement_v1.types.ManagedService` The full representation of a Service that is managed by
                   Google Service Management.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.CreateServiceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.CreateServiceRequest):
            request = servicemanager.CreateServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service is not None:
                request.service = service

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_service]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resources.ManagedService,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def delete_service(
        self,
        request: Union[servicemanager.DeleteServiceRequest, dict] = None,
        *,
        service_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Deletes a managed service. This method will change the service
        to the ``Soft-Delete`` state for 30 days. Within this period,
        service producers may call
        [UndeleteService][google.api.servicemanagement.v1.ServiceManager.UndeleteService]
        to restore the service. After 30 days, the service will be
        permanently deleted.

        Operation<response: google.protobuf.Empty>


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_delete_service():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.DeleteServiceRequest(
                    service_name="service_name_value",
                )

                # Make the request
                operation = client.delete_service(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.DeleteServiceRequest, dict]):
                The request object. Request message for DeleteService
                method.
            service_name (str):
                Required. The name of the service. See the
                `overview </service-management/overview>`__ for naming
                requirements. For example: ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.DeleteServiceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.DeleteServiceRequest):
            request = servicemanager.DeleteServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_name is not None:
                request.service_name = service_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_service]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def undelete_service(
        self,
        request: Union[servicemanager.UndeleteServiceRequest, dict] = None,
        *,
        service_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Revives a previously deleted managed service. The
        method restores the service using the configuration at
        the time the service was deleted. The target service
        must exist and must have been deleted within the last 30
        days.

        Operation<response: UndeleteServiceResponse>


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_undelete_service():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.UndeleteServiceRequest(
                    service_name="service_name_value",
                )

                # Make the request
                operation = client.undelete_service(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.UndeleteServiceRequest, dict]):
                The request object. Request message for UndeleteService
                method.
            service_name (str):
                Required. The name of the service. See the
                `overview </service-management/overview>`__ for naming
                requirements. For example: ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.servicemanagement_v1.types.UndeleteServiceResponse`
                Response message for UndeleteService method.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.UndeleteServiceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.UndeleteServiceRequest):
            request = servicemanager.UndeleteServiceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_name is not None:
                request.service_name = service_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.undelete_service]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            servicemanager.UndeleteServiceResponse,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_service_configs(
        self,
        request: Union[servicemanager.ListServiceConfigsRequest, dict] = None,
        *,
        service_name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServiceConfigsPager:
        r"""Lists the history of the service configuration for a
        managed service, from the newest to the oldest.


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_list_service_configs():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.ListServiceConfigsRequest(
                    service_name="service_name_value",
                )

                # Make the request
                page_result = client.list_service_configs(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.ListServiceConfigsRequest, dict]):
                The request object. Request message for
                ListServiceConfigs method.
            service_name (str):
                Required. The name of the service. See the
                `overview </service-management/overview>`__ for naming
                requirements. For example: ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.servicemanagement_v1.services.service_manager.pagers.ListServiceConfigsPager:
                Response message for
                ListServiceConfigs method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.ListServiceConfigsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.ListServiceConfigsRequest):
            request = servicemanager.ListServiceConfigsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_name is not None:
                request.service_name = service_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_service_configs]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListServiceConfigsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_service_config(
        self,
        request: Union[servicemanager.GetServiceConfigRequest, dict] = None,
        *,
        service_name: str = None,
        config_id: str = None,
        view: servicemanager.GetServiceConfigRequest.ConfigView = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service_pb2.Service:
        r"""Gets a service configuration (version) for a managed
        service.


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_get_service_config():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.GetServiceConfigRequest(
                    service_name="service_name_value",
                    config_id="config_id_value",
                )

                # Make the request
                response = client.get_service_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.GetServiceConfigRequest, dict]):
                The request object. Request message for GetServiceConfig
                method.
            service_name (str):
                Required. The name of the service. See the
                `overview </service-management/overview>`__ for naming
                requirements. For example: ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config_id (str):
                Required. The id of the service configuration resource.

                This field must be specified for the server to return
                all fields, including ``SourceInfo``.

                This corresponds to the ``config_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            view (google.cloud.servicemanagement_v1.types.GetServiceConfigRequest.ConfigView):
                Specifies which parts of the Service
                Config should be returned in the
                response.

                This corresponds to the ``view`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.service_pb2.Service:
                Service is the root object of Google service configuration schema. It
                   describes basic information about a service, such as
                   the name and the title, and delegates other aspects
                   to sub-sections. Each sub-section is either a proto
                   message or a repeated proto message that configures a
                   specific aspect, such as auth. See each proto message
                   definition for details.

                   Example:

                      type: google.api.Service name:
                      calendar.googleapis.com title: Google Calendar API
                      apis: - name: google.calendar.v3.Calendar
                      authentication: providers: - id:
                      google_calendar_auth jwks_uri:
                      https://www.googleapis.com/oauth2/v1/certs issuer:
                      https://securetoken.google.com rules: - selector:
                      "*" requirements: provider_id:
                      google_calendar_auth

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, config_id, view])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.GetServiceConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.GetServiceConfigRequest):
            request = servicemanager.GetServiceConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_name is not None:
                request.service_name = service_name
            if config_id is not None:
                request.config_id = config_id
            if view is not None:
                request.view = view

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_service_config]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_service_config(
        self,
        request: Union[servicemanager.CreateServiceConfigRequest, dict] = None,
        *,
        service_name: str = None,
        service_config: service_pb2.Service = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service_pb2.Service:
        r"""Creates a new service configuration (version) for a managed
        service. This method only stores the service configuration. To
        roll out the service configuration to backend systems please
        call
        [CreateServiceRollout][google.api.servicemanagement.v1.ServiceManager.CreateServiceRollout].

        Only the 100 most recent service configurations and ones
        referenced by existing rollouts are kept for each service. The
        rest will be deleted eventually.


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_create_service_config():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.CreateServiceConfigRequest(
                    service_name="service_name_value",
                )

                # Make the request
                response = client.create_service_config(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.CreateServiceConfigRequest, dict]):
                The request object. Request message for
                CreateServiceConfig method.
            service_name (str):
                Required. The name of the service. See the
                `overview </service-management/overview>`__ for naming
                requirements. For example: ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service_config (google.api.service_pb2.Service):
                Required. The service configuration
                resource.

                This corresponds to the ``service_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api.service_pb2.Service:
                Service is the root object of Google service configuration schema. It
                   describes basic information about a service, such as
                   the name and the title, and delegates other aspects
                   to sub-sections. Each sub-section is either a proto
                   message or a repeated proto message that configures a
                   specific aspect, such as auth. See each proto message
                   definition for details.

                   Example:

                      type: google.api.Service name:
                      calendar.googleapis.com title: Google Calendar API
                      apis: - name: google.calendar.v3.Calendar
                      authentication: providers: - id:
                      google_calendar_auth jwks_uri:
                      https://www.googleapis.com/oauth2/v1/certs issuer:
                      https://securetoken.google.com rules: - selector:
                      "*" requirements: provider_id:
                      google_calendar_auth

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, service_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.CreateServiceConfigRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.CreateServiceConfigRequest):
            request = servicemanager.CreateServiceConfigRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_name is not None:
                request.service_name = service_name
            if service_config is not None:
                request.service_config = service_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_service_config]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def submit_config_source(
        self,
        request: Union[servicemanager.SubmitConfigSourceRequest, dict] = None,
        *,
        service_name: str = None,
        config_source: resources.ConfigSource = None,
        validate_only: bool = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new service configuration (version) for a managed
        service based on user-supplied configuration source files (for
        example: OpenAPI Specification). This method stores the source
        configurations as well as the generated service configuration.
        To rollout the service configuration to other services, please
        call
        [CreateServiceRollout][google.api.servicemanagement.v1.ServiceManager.CreateServiceRollout].

        Only the 100 most recent configuration sources and ones
        referenced by existing service configurtions are kept for each
        service. The rest will be deleted eventually.

        Operation<response: SubmitConfigSourceResponse>


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_submit_config_source():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.SubmitConfigSourceRequest(
                    service_name="service_name_value",
                )

                # Make the request
                operation = client.submit_config_source(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.SubmitConfigSourceRequest, dict]):
                The request object. Request message for
                SubmitConfigSource method.
            service_name (str):
                Required. The name of the service. See the
                `overview </service-management/overview>`__ for naming
                requirements. For example: ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config_source (google.cloud.servicemanagement_v1.types.ConfigSource):
                Required. The source configuration
                for the service.

                This corresponds to the ``config_source`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            validate_only (bool):
                Optional. If set, this will result in the generation of
                a ``google.api.Service`` configuration based on the
                ``ConfigSource`` provided, but the generated config and
                the sources will NOT be persisted.

                This corresponds to the ``validate_only`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.servicemanagement_v1.types.SubmitConfigSourceResponse`
                Response message for SubmitConfigSource method.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, config_source, validate_only])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.SubmitConfigSourceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.SubmitConfigSourceRequest):
            request = servicemanager.SubmitConfigSourceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_name is not None:
                request.service_name = service_name
            if config_source is not None:
                request.config_source = config_source
            if validate_only is not None:
                request.validate_only = validate_only

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.submit_config_source]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            servicemanager.SubmitConfigSourceResponse,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def list_service_rollouts(
        self,
        request: Union[servicemanager.ListServiceRolloutsRequest, dict] = None,
        *,
        service_name: str = None,
        filter: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServiceRolloutsPager:
        r"""Lists the history of the service configuration
        rollouts for a managed service, from the newest to the
        oldest.


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_list_service_rollouts():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.ListServiceRolloutsRequest(
                    service_name="service_name_value",
                    filter="filter_value",
                )

                # Make the request
                page_result = client.list_service_rollouts(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.ListServiceRolloutsRequest, dict]):
                The request object. Request message for
                'ListServiceRollouts'
            service_name (str):
                Required. The name of the service. See the
                `overview </service-management/overview>`__ for naming
                requirements. For example: ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                Required. Use ``filter`` to return subset of rollouts.
                The following filters are supported: -- To limit the
                results to only those in
                `status <google.api.servicemanagement.v1.RolloutStatus>`__
                'SUCCESS', use filter='status=SUCCESS' -- To limit the
                results to those in
                `status <google.api.servicemanagement.v1.RolloutStatus>`__
                'CANCELLED' or 'FAILED', use filter='status=CANCELLED OR
                status=FAILED'

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.servicemanagement_v1.services.service_manager.pagers.ListServiceRolloutsPager:
                Response message for
                ListServiceRollouts method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.ListServiceRolloutsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.ListServiceRolloutsRequest):
            request = servicemanager.ListServiceRolloutsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_name is not None:
                request.service_name = service_name
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_service_rollouts]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListServiceRolloutsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_service_rollout(
        self,
        request: Union[servicemanager.GetServiceRolloutRequest, dict] = None,
        *,
        service_name: str = None,
        rollout_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Rollout:
        r"""Gets a service configuration
        [rollout][google.api.servicemanagement.v1.Rollout].


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_get_service_rollout():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.GetServiceRolloutRequest(
                    service_name="service_name_value",
                    rollout_id="rollout_id_value",
                )

                # Make the request
                response = client.get_service_rollout(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.GetServiceRolloutRequest, dict]):
                The request object. Request message for
                GetServiceRollout method.
            service_name (str):
                Required. The name of the service. See the
                `overview </service-management/overview>`__ for naming
                requirements. For example: ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rollout_id (str):
                Required. The id of the rollout
                resource.

                This corresponds to the ``rollout_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.servicemanagement_v1.types.Rollout:
                A rollout resource that defines how
                service configuration versions are
                pushed to control plane systems.
                Typically, you create a new version of
                the service config, and then create a
                Rollout to push the service config.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, rollout_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.GetServiceRolloutRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.GetServiceRolloutRequest):
            request = servicemanager.GetServiceRolloutRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_name is not None:
                request.service_name = service_name
            if rollout_id is not None:
                request.rollout_id = rollout_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_service_rollout]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_service_rollout(
        self,
        request: Union[servicemanager.CreateServiceRolloutRequest, dict] = None,
        *,
        service_name: str = None,
        rollout: resources.Rollout = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new service configuration rollout. Based on
        rollout, the Google Service Management will roll out the
        service configurations to different backend services.
        For example, the logging configuration will be pushed to
        Google Cloud Logging.

        Please note that any previous pending and running
        Rollouts and associated Operations will be automatically
        cancelled so that the latest Rollout will not be blocked
        by previous Rollouts.

        Only the 100 most recent (in any state) and the last 10
        successful (if not already part of the set of 100 most
        recent) rollouts are kept for each service. The rest
        will be deleted eventually.

        Operation<response: Rollout>


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_create_service_rollout():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.CreateServiceRolloutRequest(
                    service_name="service_name_value",
                )

                # Make the request
                operation = client.create_service_rollout(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.CreateServiceRolloutRequest, dict]):
                The request object. Request message for
                'CreateServiceRollout'
            service_name (str):
                Required. The name of the service. See the
                `overview </service-management/overview>`__ for naming
                requirements. For example: ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rollout (google.cloud.servicemanagement_v1.types.Rollout):
                Required. The rollout resource. The ``service_name``
                field is output only.

                This corresponds to the ``rollout`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.servicemanagement_v1.types.Rollout` A rollout resource that defines how service configuration versions are pushed
                   to control plane systems. Typically, you create a new
                   version of the service config, and then create a
                   Rollout to push the service config.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, rollout])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.CreateServiceRolloutRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.CreateServiceRolloutRequest):
            request = servicemanager.CreateServiceRolloutRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if service_name is not None:
                request.service_name = service_name
            if rollout is not None:
                request.rollout = rollout

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_service_rollout]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            resources.Rollout,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    def generate_config_report(
        self,
        request: Union[servicemanager.GenerateConfigReportRequest, dict] = None,
        *,
        new_config: any_pb2.Any = None,
        old_config: any_pb2.Any = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> servicemanager.GenerateConfigReportResponse:
        r"""Generates and returns a report (errors, warnings and changes
        from existing configurations) associated with
        GenerateConfigReportRequest.new_value

        If GenerateConfigReportRequest.old_value is specified,
        GenerateConfigReportRequest will contain a single ChangeReport
        based on the comparison between
        GenerateConfigReportRequest.new_value and
        GenerateConfigReportRequest.old_value. If
        GenerateConfigReportRequest.old_value is not specified, this
        method will compare GenerateConfigReportRequest.new_value with
        the last pushed service configuration.


        .. code-block:: python

            from google.cloud import servicemanagement_v1

            def sample_generate_config_report():
                # Create a client
                client = servicemanagement_v1.ServiceManagerClient()

                # Initialize request argument(s)
                request = servicemanagement_v1.GenerateConfigReportRequest(
                )

                # Make the request
                response = client.generate_config_report(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.servicemanagement_v1.types.GenerateConfigReportRequest, dict]):
                The request object. Request message for
                GenerateConfigReport method.
            new_config (google.protobuf.any_pb2.Any):
                Required. Service configuration for which we want to
                generate the report. For this version of API, the
                supported types are
                [google.api.servicemanagement.v1.ConfigRef][google.api.servicemanagement.v1.ConfigRef],
                [google.api.servicemanagement.v1.ConfigSource][google.api.servicemanagement.v1.ConfigSource],
                and [google.api.Service][google.api.Service]

                This corresponds to the ``new_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            old_config (google.protobuf.any_pb2.Any):
                Optional. Service configuration against which the
                comparison will be done. For this version of API, the
                supported types are
                [google.api.servicemanagement.v1.ConfigRef][google.api.servicemanagement.v1.ConfigRef],
                [google.api.servicemanagement.v1.ConfigSource][google.api.servicemanagement.v1.ConfigSource],
                and [google.api.Service][google.api.Service]

                This corresponds to the ``old_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.servicemanagement_v1.types.GenerateConfigReportResponse:
                Response message for
                GenerateConfigReport method.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([new_config, old_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a servicemanager.GenerateConfigReportRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, servicemanager.GenerateConfigReportRequest):
            request = servicemanager.GenerateConfigReportRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if new_config is not None:
                request.new_config = new_config
            if old_config is not None:
                request.old_config = old_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.generate_config_report]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-service-management",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ServiceManagerClient",)
