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
import warnings

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

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
from .transports.grpc_asyncio import ServiceManagerGrpcAsyncIOTransport
from .client import ServiceManagerClient


class ServiceManagerAsyncClient:
    """`Google Service Management
    API <https://cloud.google.com/service-management/overview>`__
    """

    _client: ServiceManagerClient

    DEFAULT_ENDPOINT = ServiceManagerClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ServiceManagerClient.DEFAULT_MTLS_ENDPOINT

    common_billing_account_path = staticmethod(
        ServiceManagerClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ServiceManagerClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ServiceManagerClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ServiceManagerClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ServiceManagerClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ServiceManagerClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ServiceManagerClient.common_project_path)
    parse_common_project_path = staticmethod(
        ServiceManagerClient.parse_common_project_path
    )
    common_location_path = staticmethod(ServiceManagerClient.common_location_path)
    parse_common_location_path = staticmethod(
        ServiceManagerClient.parse_common_location_path
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
            ServiceManagerAsyncClient: The constructed client.
        """
        return ServiceManagerClient.from_service_account_info.__func__(ServiceManagerAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ServiceManagerAsyncClient: The constructed client.
        """
        return ServiceManagerClient.from_service_account_file.__func__(ServiceManagerAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ServiceManagerTransport:
        """Returns the transport used by the client instance.

        Returns:
            ServiceManagerTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ServiceManagerClient).get_transport_class, type(ServiceManagerClient)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ServiceManagerTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the service manager client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ServiceManagerTransport]): The
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
        self._client = ServiceManagerClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def list_services(
        self,
        request: servicemanager.ListServicesRequest = None,
        *,
        producer_project_id: str = None,
        consumer_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServicesAsyncPager:
        r"""Lists managed services.

        Returns all public services. For authenticated users, also
        returns all services the calling user has
        "servicemanagement.services.get" permission for.

        **BETA:** If the caller specifies the ``consumer_id``, it
        returns only the services enabled on the consumer. The
        ``consumer_id`` must have the format of "project:{PROJECT-ID}".

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.ListServicesRequest`):
                The request object. Request message for `ListServices`
                method.
            producer_project_id (:class:`str`):
                Include services produced by the
                specified project.

                This corresponds to the ``producer_project_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            consumer_id (:class:`str`):
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
            google.cloud.servicemanagement_v1.services.service_manager.pagers.ListServicesAsyncPager:
                Response message for ListServices method.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([producer_project_id, consumer_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.ListServicesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if producer_project_id is not None:
            request.producer_project_id = producer_project_id
        if consumer_id is not None:
            request.consumer_id = consumer_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_services,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListServicesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_service(
        self,
        request: servicemanager.GetServiceRequest = None,
        *,
        service_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.ManagedService:
        r"""Gets a managed service. Authentication is required
        unless the service is public.

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.GetServiceRequest`):
                The request object. Request message for `GetService`
                method.
            service_name (:class:`str`):
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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.GetServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_name is not None:
            request.service_name = service_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_service,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_service(
        self,
        request: servicemanager.CreateServiceRequest = None,
        *,
        service: resources.ManagedService = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Creates a new managed service.
        Please note one producer project can own no more than 20
        services.
        Operation<response: ManagedService>

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.CreateServiceRequest`):
                The request object. Request message for CreateService
                method.
            service (:class:`google.cloud.servicemanagement_v1.types.ManagedService`):
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
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.servicemanagement_v1.types.ManagedService` The full representation of a Service that is managed by
                   Google Service Management.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.CreateServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service is not None:
            request.service = service

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_service,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            resources.ManagedService,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def delete_service(
        self,
        request: servicemanager.DeleteServiceRequest = None,
        *,
        service_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Deletes a managed service. This method will change the service
        to the ``Soft-Delete`` state for 30 days. Within this period,
        service producers may call
        [UndeleteService][google.api.servicemanagement.v1.ServiceManager.UndeleteService]
        to restore the service. After 30 days, the service will be
        permanently deleted.

        Operation<response: google.protobuf.Empty>

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.DeleteServiceRequest`):
                The request object. Request message for DeleteService
                method.
            service_name (:class:`str`):
                Required. The name of the service. See the
                `overview <https://cloud.google.com/service-management/overview>`__
                for naming requirements. For example:
                ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
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
        has_flattened_params = any([service_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.DeleteServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_name is not None:
            request.service_name = service_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_service,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def undelete_service(
        self,
        request: servicemanager.UndeleteServiceRequest = None,
        *,
        service_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Revives a previously deleted managed service. The
        method restores the service using the configuration at
        the time the service was deleted. The target service
        must exist and must have been deleted within the last 30
        days.

        Operation<response: UndeleteServiceResponse>

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.UndeleteServiceRequest`):
                The request object. Request message for UndeleteService
                method.
            service_name (:class:`str`):
                Required. The name of the service. See the
                `overview <https://cloud.google.com/service-management/overview>`__
                for naming requirements. For example:
                ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
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
                :class:`google.cloud.servicemanagement_v1.types.UndeleteServiceResponse`
                Response message for UndeleteService method.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.UndeleteServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_name is not None:
            request.service_name = service_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.undelete_service,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            servicemanager.UndeleteServiceResponse,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_service_configs(
        self,
        request: servicemanager.ListServiceConfigsRequest = None,
        *,
        service_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServiceConfigsAsyncPager:
        r"""Lists the history of the service configuration for a
        managed service, from the newest to the oldest.

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.ListServiceConfigsRequest`):
                The request object. Request message for
                ListServiceConfigs method.
            service_name (:class:`str`):
                Required. The name of the service. See the
                `overview <https://cloud.google.com/service-management/overview>`__
                for naming requirements. For example:
                ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.servicemanagement_v1.services.service_manager.pagers.ListServiceConfigsAsyncPager:
                Response message for
                ListServiceConfigs method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.ListServiceConfigsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_name is not None:
            request.service_name = service_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_service_configs,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListServiceConfigsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_service_config(
        self,
        request: servicemanager.GetServiceConfigRequest = None,
        *,
        service_name: str = None,
        config_id: str = None,
        view: servicemanager.GetServiceConfigRequest.ConfigView = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service_pb2.Service:
        r"""Gets a service configuration (version) for a managed
        service.

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.GetServiceConfigRequest`):
                The request object. Request message for GetServiceConfig
                method.
            service_name (:class:`str`):
                Required. The name of the service. See the
                `overview <https://cloud.google.com/service-management/overview>`__
                for naming requirements. For example:
                ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config_id (:class:`str`):
                Required. The id of the service configuration resource.

                This field must be specified for the server to return
                all fields, including ``SourceInfo``.

                This corresponds to the ``config_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            view (:class:`google.cloud.servicemanagement_v1.types.GetServiceConfigRequest.ConfigView`):
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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, config_id, view])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_service_config,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_service_config(
        self,
        request: servicemanager.CreateServiceConfigRequest = None,
        *,
        service_name: str = None,
        service_config: service_pb2.Service = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
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

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.CreateServiceConfigRequest`):
                The request object. Request message for
                CreateServiceConfig method.
            service_name (:class:`str`):
                Required. The name of the service. See the
                `overview <https://cloud.google.com/service-management/overview>`__
                for naming requirements. For example:
                ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service_config (:class:`google.api.service_pb2.Service`):
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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, service_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.CreateServiceConfigRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_name is not None:
            request.service_name = service_name
        if service_config is not None:
            request.service_config = service_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_service_config,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def submit_config_source(
        self,
        request: servicemanager.SubmitConfigSourceRequest = None,
        *,
        service_name: str = None,
        config_source: resources.ConfigSource = None,
        validate_only: bool = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
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

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.SubmitConfigSourceRequest`):
                The request object. Request message for
                SubmitConfigSource method.
            service_name (:class:`str`):
                Required. The name of the service. See the
                `overview <https://cloud.google.com/service-management/overview>`__
                for naming requirements. For example:
                ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config_source (:class:`google.cloud.servicemanagement_v1.types.ConfigSource`):
                Required. The source configuration
                for the service.

                This corresponds to the ``config_source`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            validate_only (:class:`bool`):
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
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.servicemanagement_v1.types.SubmitConfigSourceResponse`
                Response message for SubmitConfigSource method.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, config_source, validate_only])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.submit_config_source,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            servicemanager.SubmitConfigSourceResponse,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def list_service_rollouts(
        self,
        request: servicemanager.ListServiceRolloutsRequest = None,
        *,
        service_name: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServiceRolloutsAsyncPager:
        r"""Lists the history of the service configuration
        rollouts for a managed service, from the newest to the
        oldest.

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.ListServiceRolloutsRequest`):
                The request object. Request message for
                'ListServiceRollouts'
            service_name (:class:`str`):
                Required. The name of the service. See the
                `overview <https://cloud.google.com/service-management/overview>`__
                for naming requirements. For example:
                ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
                Required. Use ``filter`` to return subset of rollouts.
                The following filters are supported: -- To limit the
                results to only those in status
                (google.api.servicemanagement.v1.RolloutStatus)
                'SUCCESS', use filter='status=SUCCESS' -- To limit the
                results to those in status
                (google.api.servicemanagement.v1.RolloutStatus)
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
            google.cloud.servicemanagement_v1.services.service_manager.pagers.ListServiceRolloutsAsyncPager:
                Response message for
                ListServiceRollouts method.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.ListServiceRolloutsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_name is not None:
            request.service_name = service_name
        if filter is not None:
            request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_service_rollouts,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListServiceRolloutsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_service_rollout(
        self,
        request: servicemanager.GetServiceRolloutRequest = None,
        *,
        service_name: str = None,
        rollout_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> resources.Rollout:
        r"""Gets a service configuration
        [rollout][google.api.servicemanagement.v1.Rollout].

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.GetServiceRolloutRequest`):
                The request object. Request message for
                GetServiceRollout method.
            service_name (:class:`str`):
                Required. The name of the service. See the
                `overview <https://cloud.google.com/service-management/overview>`__
                for naming requirements. For example:
                ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rollout_id (:class:`str`):
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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, rollout_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.GetServiceRolloutRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_name is not None:
            request.service_name = service_name
        if rollout_id is not None:
            request.rollout_id = rollout_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_service_rollout,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_service_rollout(
        self,
        request: servicemanager.CreateServiceRolloutRequest = None,
        *,
        service_name: str = None,
        rollout: resources.Rollout = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
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

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.CreateServiceRolloutRequest`):
                The request object. Request message for
                'CreateServiceRollout'
            service_name (:class:`str`):
                Required. The name of the service. See the
                `overview <https://cloud.google.com/service-management/overview>`__
                for naming requirements. For example:
                ``example.googleapis.com``.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            rollout (:class:`google.cloud.servicemanagement_v1.types.Rollout`):
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
            google.api_core.operation_async.AsyncOperation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.cloud.servicemanagement_v1.types.Rollout` A rollout resource that defines how service configuration versions are pushed
                   to control plane systems. Typically, you create a new
                   version of the service config, and then create a
                   Rollout to push the service config.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, rollout])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.CreateServiceRolloutRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_name is not None:
            request.service_name = service_name
        if rollout is not None:
            request.rollout = rollout

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_service_rollout,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            resources.Rollout,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def generate_config_report(
        self,
        request: servicemanager.GenerateConfigReportRequest = None,
        *,
        new_config: any_pb2.Any = None,
        old_config: any_pb2.Any = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
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

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.GenerateConfigReportRequest`):
                The request object. Request message for
                GenerateConfigReport method.
            new_config (:class:`google.protobuf.any_pb2.Any`):
                Required. Service configuration for which we want to
                generate the report. For this version of API, the
                supported types are
                [google.api.servicemanagement.v1.ConfigRef][google.api.servicemanagement.v1.ConfigRef],
                [google.api.servicemanagement.v1.ConfigSource][google.api.servicemanagement.v1.ConfigSource],
                and [google.api.Service][google.api.Service]

                This corresponds to the ``new_config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            old_config (:class:`google.protobuf.any_pb2.Any`):
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
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([new_config, old_config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.GenerateConfigReportRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if new_config is not None:
            request.new_config = new_config
        if old_config is not None:
            request.old_config = old_config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.generate_config_report,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def enable_service(
        self,
        request: servicemanager.EnableServiceRequest = None,
        *,
        service_name: str = None,
        consumer_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Enables a
        [service][google.api.servicemanagement.v1.ManagedService] for a
        project, so it can be used for the project. See `Cloud Auth
        Guide <https://cloud.google.com/docs/authentication>`__ for more
        information.

        Operation<response: EnableServiceResponse>

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.EnableServiceRequest`):
                The request object. Request message for EnableService
                method.
            service_name (:class:`str`):
                Required. Name of the service to
                enable. Specifying an unknown service
                name will cause the request to fail.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            consumer_id (:class:`str`):
                Required. The identity of consumer resource which
                service enablement will be applied to.

                The Google Service Management implementation accepts the
                following forms:

                -  "project:<project_id>"

                Note: this is made compatible with
                google.api.servicecontrol.v1.Operation.consumer_id.

                This corresponds to the ``consumer_id`` field
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
                :class:`google.cloud.servicemanagement_v1.types.EnableServiceResponse`
                Operation payload for EnableService method.

        """
        warnings.warn(
            "ServiceManagerAsyncClient.enable_service is deprecated", DeprecationWarning
        )

        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, consumer_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.EnableServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_name is not None:
            request.service_name = service_name
        if consumer_id is not None:
            request.consumer_id = consumer_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.enable_service,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            servicemanager.EnableServiceResponse,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response

    async def disable_service(
        self,
        request: servicemanager.DisableServiceRequest = None,
        *,
        service_name: str = None,
        consumer_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation_async.AsyncOperation:
        r"""Disables a
        [service][google.api.servicemanagement.v1.ManagedService] for a
        project, so it can no longer be be used for the project. It
        prevents accidental usage that may cause unexpected billing
        charges or security leaks.

        Operation<response: DisableServiceResponse>

        Args:
            request (:class:`google.cloud.servicemanagement_v1.types.DisableServiceRequest`):
                The request object. Request message for DisableService
                method.
            service_name (:class:`str`):
                Required. Name of the service to
                disable. Specifying an unknown service
                name will cause the request to fail.

                This corresponds to the ``service_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            consumer_id (:class:`str`):
                Required. The identity of consumer resource which
                service disablement will be applied to.

                The Google Service Management implementation accepts the
                following forms:

                -  "project:<project_id>"

                Note: this is made compatible with
                google.api.servicecontrol.v1.Operation.consumer_id.

                This corresponds to the ``consumer_id`` field
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
                :class:`google.cloud.servicemanagement_v1.types.DisableServiceResponse`
                Operation payload for DisableService method.

        """
        warnings.warn(
            "ServiceManagerAsyncClient.disable_service is deprecated",
            DeprecationWarning,
        )

        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_name, consumer_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = servicemanager.DisableServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_name is not None:
            request.service_name = service_name
        if consumer_id is not None:
            request.consumer_id = consumer_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.disable_service,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Wrap the response in an operation future.
        response = operation_async.from_gapic(
            response,
            self._client._transport.operations_client,
            servicemanager.DisableServiceResponse,
            metadata_type=resources.OperationMetadata,
        )

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-service-management",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ServiceManagerAsyncClient",)
