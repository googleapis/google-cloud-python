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

from google.cloud.monitoring_v3.services.service_monitoring_service import pagers
from google.cloud.monitoring_v3.types import service
from google.cloud.monitoring_v3.types import service as gm_service
from google.cloud.monitoring_v3.types import service_service
from google.protobuf import duration_pb2  # type: ignore
from google.type import calendar_period_pb2  # type: ignore
from .transports.base import ServiceMonitoringServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ServiceMonitoringServiceGrpcAsyncIOTransport
from .client import ServiceMonitoringServiceClient


class ServiceMonitoringServiceAsyncClient:
    """The Cloud Monitoring Service-Oriented Monitoring API has endpoints
    for managing and querying aspects of a workspace's services. These
    include the ``Service``'s monitored resources, its Service-Level
    Objectives, and a taxonomy of categorized Health Metrics.
    """

    _client: ServiceMonitoringServiceClient

    DEFAULT_ENDPOINT = ServiceMonitoringServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ServiceMonitoringServiceClient.DEFAULT_MTLS_ENDPOINT

    service_path = staticmethod(ServiceMonitoringServiceClient.service_path)
    parse_service_path = staticmethod(ServiceMonitoringServiceClient.parse_service_path)
    service_level_objective_path = staticmethod(
        ServiceMonitoringServiceClient.service_level_objective_path
    )
    parse_service_level_objective_path = staticmethod(
        ServiceMonitoringServiceClient.parse_service_level_objective_path
    )
    common_billing_account_path = staticmethod(
        ServiceMonitoringServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ServiceMonitoringServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ServiceMonitoringServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ServiceMonitoringServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ServiceMonitoringServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ServiceMonitoringServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(
        ServiceMonitoringServiceClient.common_project_path
    )
    parse_common_project_path = staticmethod(
        ServiceMonitoringServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(
        ServiceMonitoringServiceClient.common_location_path
    )
    parse_common_location_path = staticmethod(
        ServiceMonitoringServiceClient.parse_common_location_path
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
            ServiceMonitoringServiceAsyncClient: The constructed client.
        """
        return ServiceMonitoringServiceClient.from_service_account_info.__func__(ServiceMonitoringServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ServiceMonitoringServiceAsyncClient: The constructed client.
        """
        return ServiceMonitoringServiceClient.from_service_account_file.__func__(ServiceMonitoringServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ServiceMonitoringServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ServiceMonitoringServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ServiceMonitoringServiceClient).get_transport_class,
        type(ServiceMonitoringServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ServiceMonitoringServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the service monitoring service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ServiceMonitoringServiceTransport]): The
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
        self._client = ServiceMonitoringServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_service(
        self,
        request: Union[service_service.CreateServiceRequest, dict] = None,
        *,
        parent: str = None,
        service: gm_service.Service = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gm_service.Service:
        r"""Create a ``Service``.

        Args:
            request (Union[google.cloud.monitoring_v3.types.CreateServiceRequest, dict]):
                The request object. The `CreateService` request.
            parent (:class:`str`):
                Required. Resource
                `name <https://cloud.google.com/monitoring/api/v3#project_name>`__
                of the parent workspace. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service (:class:`google.cloud.monitoring_v3.types.Service`):
                Required. The ``Service`` to create.
                This corresponds to the ``service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.Service:
                A Service is a discrete, autonomous, and network-accessible unit, designed
                   to solve an individual concern
                   ([Wikipedia](https://en.wikipedia.org/wiki/Service-orientation)).
                   In Cloud Monitoring, a Service acts as the root
                   resource under which operational aspects of the
                   service are accessible.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, service])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service_service.CreateServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if service is not None:
            request.service = service

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_service,
            default_timeout=30.0,
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

    async def get_service(
        self,
        request: Union[service_service.GetServiceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.Service:
        r"""Get the named ``Service``.

        Args:
            request (Union[google.cloud.monitoring_v3.types.GetServiceRequest, dict]):
                The request object. The `GetService` request.
            name (:class:`str`):
                Required. Resource name of the ``Service``. The format
                is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.Service:
                A Service is a discrete, autonomous, and network-accessible unit, designed
                   to solve an individual concern
                   ([Wikipedia](https://en.wikipedia.org/wiki/Service-orientation)).
                   In Cloud Monitoring, a Service acts as the root
                   resource under which operational aspects of the
                   service are accessible.

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

        request = service_service.GetServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_service,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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

    async def list_services(
        self,
        request: Union[service_service.ListServicesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServicesAsyncPager:
        r"""List ``Service``\ s for this workspace.

        Args:
            request (Union[google.cloud.monitoring_v3.types.ListServicesRequest, dict]):
                The request object. The `ListServices` request.
            parent (:class:`str`):
                Required. Resource name of the parent containing the
                listed services, either a
                `project <https://cloud.google.com/monitoring/api/v3#project_name>`__
                or a Monitoring Workspace. The formats are:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]
                    workspaces/[HOST_PROJECT_ID_OR_NUMBER]

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.service_monitoring_service.pagers.ListServicesAsyncPager:
                The ListServices response.

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

        request = service_service.ListServicesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_services,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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
        response = pagers.ListServicesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_service(
        self,
        request: Union[service_service.UpdateServiceRequest, dict] = None,
        *,
        service: gm_service.Service = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gm_service.Service:
        r"""Update this ``Service``.

        Args:
            request (Union[google.cloud.monitoring_v3.types.UpdateServiceRequest, dict]):
                The request object. The `UpdateService` request.
            service (:class:`google.cloud.monitoring_v3.types.Service`):
                Required. The ``Service`` to draw updates from. The
                given ``name`` specifies the resource to update.

                This corresponds to the ``service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.Service:
                A Service is a discrete, autonomous, and network-accessible unit, designed
                   to solve an individual concern
                   ([Wikipedia](https://en.wikipedia.org/wiki/Service-orientation)).
                   In Cloud Monitoring, a Service acts as the root
                   resource under which operational aspects of the
                   service are accessible.

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

        request = service_service.UpdateServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service is not None:
            request.service = service

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_service,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("service.name", request.service.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_service(
        self,
        request: Union[service_service.DeleteServiceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Soft delete this ``Service``.

        Args:
            request (Union[google.cloud.monitoring_v3.types.DeleteServiceRequest, dict]):
                The request object. The `DeleteService` request.
            name (:class:`str`):
                Required. Resource name of the ``Service`` to delete.
                The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]

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

        request = service_service.DeleteServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_service,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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

    async def create_service_level_objective(
        self,
        request: Union[service_service.CreateServiceLevelObjectiveRequest, dict] = None,
        *,
        parent: str = None,
        service_level_objective: service.ServiceLevelObjective = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.ServiceLevelObjective:
        r"""Create a ``ServiceLevelObjective`` for the given ``Service``.

        Args:
            request (Union[google.cloud.monitoring_v3.types.CreateServiceLevelObjectiveRequest, dict]):
                The request object. The `CreateServiceLevelObjective`
                request.
            parent (:class:`str`):
                Required. Resource name of the parent ``Service``. The
                format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service_level_objective (:class:`google.cloud.monitoring_v3.types.ServiceLevelObjective`):
                Required. The ``ServiceLevelObjective`` to create. The
                provided ``name`` will be respected if no
                ``ServiceLevelObjective`` exists with this name.

                This corresponds to the ``service_level_objective`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.ServiceLevelObjective:
                A Service-Level Objective (SLO)
                describes a level of desired good
                service. It consists of a service-level
                indicator (SLI), a performance goal, and
                a period over which the objective is to
                be evaluated against that goal. The SLO
                can use SLIs defined in a number of
                different manners. Typical SLOs might
                include "99% of requests in each rolling
                week have latency below 200
                milliseconds" or "99.5% of requests in
                each calendar month return
                successfully."

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, service_level_objective])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service_service.CreateServiceLevelObjectiveRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if service_level_objective is not None:
            request.service_level_objective = service_level_objective

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_service_level_objective,
            default_timeout=30.0,
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

    async def get_service_level_objective(
        self,
        request: Union[service_service.GetServiceLevelObjectiveRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.ServiceLevelObjective:
        r"""Get a ``ServiceLevelObjective`` by name.

        Args:
            request (Union[google.cloud.monitoring_v3.types.GetServiceLevelObjectiveRequest, dict]):
                The request object. The `GetServiceLevelObjective`
                request.
            name (:class:`str`):
                Required. Resource name of the ``ServiceLevelObjective``
                to get. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]/serviceLevelObjectives/[SLO_NAME]

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.ServiceLevelObjective:
                A Service-Level Objective (SLO)
                describes a level of desired good
                service. It consists of a service-level
                indicator (SLI), a performance goal, and
                a period over which the objective is to
                be evaluated against that goal. The SLO
                can use SLIs defined in a number of
                different manners. Typical SLOs might
                include "99% of requests in each rolling
                week have latency below 200
                milliseconds" or "99.5% of requests in
                each calendar month return
                successfully."

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

        request = service_service.GetServiceLevelObjectiveRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_service_level_objective,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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

    async def list_service_level_objectives(
        self,
        request: Union[service_service.ListServiceLevelObjectivesRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServiceLevelObjectivesAsyncPager:
        r"""List the ``ServiceLevelObjective``\ s for the given ``Service``.

        Args:
            request (Union[google.cloud.monitoring_v3.types.ListServiceLevelObjectivesRequest, dict]):
                The request object. The `ListServiceLevelObjectives`
                request.
            parent (:class:`str`):
                Required. Resource name of the parent containing the
                listed SLOs, either a project or a Monitoring Workspace.
                The formats are:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]
                    workspaces/[HOST_PROJECT_ID_OR_NUMBER]/services/-

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.services.service_monitoring_service.pagers.ListServiceLevelObjectivesAsyncPager:
                The ListServiceLevelObjectives response.

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

        request = service_service.ListServiceLevelObjectivesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_service_level_objectives,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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
        response = pagers.ListServiceLevelObjectivesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def update_service_level_objective(
        self,
        request: Union[service_service.UpdateServiceLevelObjectiveRequest, dict] = None,
        *,
        service_level_objective: service.ServiceLevelObjective = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.ServiceLevelObjective:
        r"""Update the given ``ServiceLevelObjective``.

        Args:
            request (Union[google.cloud.monitoring_v3.types.UpdateServiceLevelObjectiveRequest, dict]):
                The request object. The `UpdateServiceLevelObjective`
                request.
            service_level_objective (:class:`google.cloud.monitoring_v3.types.ServiceLevelObjective`):
                Required. The ``ServiceLevelObjective`` to draw updates
                from. The given ``name`` specifies the resource to
                update.

                This corresponds to the ``service_level_objective`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.monitoring_v3.types.ServiceLevelObjective:
                A Service-Level Objective (SLO)
                describes a level of desired good
                service. It consists of a service-level
                indicator (SLI), a performance goal, and
                a period over which the objective is to
                be evaluated against that goal. The SLO
                can use SLIs defined in a number of
                different manners. Typical SLOs might
                include "99% of requests in each rolling
                week have latency below 200
                milliseconds" or "99.5% of requests in
                each calendar month return
                successfully."

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([service_level_objective])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = service_service.UpdateServiceLevelObjectiveRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_level_objective is not None:
            request.service_level_objective = service_level_objective

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_service_level_objective,
            default_timeout=30.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (
                    (
                        "service_level_objective.name",
                        request.service_level_objective.name,
                    ),
                )
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def delete_service_level_objective(
        self,
        request: Union[service_service.DeleteServiceLevelObjectiveRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Delete the given ``ServiceLevelObjective``.

        Args:
            request (Union[google.cloud.monitoring_v3.types.DeleteServiceLevelObjectiveRequest, dict]):
                The request object. The `DeleteServiceLevelObjective`
                request.
            name (:class:`str`):
                Required. Resource name of the ``ServiceLevelObjective``
                to delete. The format is:

                ::

                    projects/[PROJECT_ID_OR_NUMBER]/services/[SERVICE_ID]/serviceLevelObjectives/[SLO_NAME]

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

        request = service_service.DeleteServiceLevelObjectiveRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_service_level_objective,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=30.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=30.0,
            ),
            default_timeout=30.0,
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
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-monitoring",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ServiceMonitoringServiceAsyncClient",)
