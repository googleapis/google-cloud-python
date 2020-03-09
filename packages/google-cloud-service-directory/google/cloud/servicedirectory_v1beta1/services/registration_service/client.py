# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.servicedirectory_v1beta1.services.registration_service import pagers
from google.cloud.servicedirectory_v1beta1.types import endpoint
from google.cloud.servicedirectory_v1beta1.types import endpoint as gcs_endpoint
from google.cloud.servicedirectory_v1beta1.types import namespace
from google.cloud.servicedirectory_v1beta1.types import namespace as gcs_namespace
from google.cloud.servicedirectory_v1beta1.types import registration_service
from google.cloud.servicedirectory_v1beta1.types import service
from google.cloud.servicedirectory_v1beta1.types import service as gcs_service
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore

from .transports.base import RegistrationServiceTransport
from .transports.grpc import RegistrationServiceGrpcTransport


class RegistrationServiceClientMeta(type):
    """Metaclass for the RegistrationService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[RegistrationServiceTransport]]
    _transport_registry["grpc"] = RegistrationServiceGrpcTransport

    def get_transport_class(
        cls, label: str = None
    ) -> Type[RegistrationServiceTransport]:
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


class RegistrationServiceClient(metaclass=RegistrationServiceClientMeta):
    """Service Directory API for registering services. It defines the
    following resource model:

    -  The API has a collection of
       [Namespace][google.cloud.servicedirectory.v1beta1.Namespace]
       resources, named ``projects/*/locations/*/namespaces/*``.

    -  Each Namespace has a collection of
       [Service][google.cloud.servicedirectory.v1beta1.Service]
       resources, named
       ``projects/*/locations/*/namespaces/*/services/*``.

    -  Each Service has a collection of
       [Endpoint][google.cloud.servicedirectory.v1beta1.Endpoint]
       resources, named
       ``projects/*/locations/*/namespaces/*/services/*/endpoints/*``.
    """

    DEFAULT_OPTIONS = ClientOptions.ClientOptions(
        api_endpoint="servicedirectory.googleapis.com"
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
    def service_path(project: str, location: str, namespace: str, service: str) -> str:
        """Return a fully-qualified service string."""
        return "projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}".format(
            project=project, location=location, namespace=namespace, service=service
        )

    @staticmethod
    def namespace_path(project: str, location: str, namespace: str) -> str:
        """Return a fully-qualified namespace string."""
        return "projects/{project}/locations/{location}/namespaces/{namespace}".format(
            project=project, location=location, namespace=namespace
        )

    @staticmethod
    def endpoint_path(
        project: str, location: str, namespace: str, service: str, endpoint: str
    ) -> str:
        """Return a fully-qualified endpoint string."""
        return "projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}/endpoints/{endpoint}".format(
            project=project,
            location=location,
            namespace=namespace,
            service=service,
            endpoint=endpoint,
        )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, RegistrationServiceTransport] = None,
        client_options: ClientOptions = DEFAULT_OPTIONS,
    ) -> None:
        """Instantiate the registration service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.RegistrationServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, RegistrationServiceTransport):
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                host=client_options.api_endpoint or "servicedirectory.googleapis.com",
            )

    def create_namespace(
        self,
        request: registration_service.CreateNamespaceRequest = None,
        *,
        parent: str = None,
        namespace: gcs_namespace.Namespace = None,
        namespace_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcs_namespace.Namespace:
        r"""Creates a namespace, and returns the new Namespace.

        Args:
            request (:class:`~.registration_service.CreateNamespaceRequest`):
                The request object. The request message for
                [RegistrationService.CreateNamespace][google.cloud.servicedirectory.v1beta1.RegistrationService.CreateNamespace].
            parent (:class:`str`):
                Required. The resource name of the
                project and location the namespace will
                be created in.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            namespace (:class:`~.gcs_namespace.Namespace`):
                Required. A namespace with initial
                fields set.
                This corresponds to the ``namespace`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            namespace_id (:class:`str`):
                Required. The Resource ID must be 1-63 characters long,
                and comply with RFC1035. Specifically, the name must be
                1-63 characters long and match the regular expression
                ``[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?`` which means the
                first character must be a lowercase letter, and all
                following characters must be a dash, lowercase letter,
                or digit, except the last character, which cannot be a
                dash.
                This corresponds to the ``namespace_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcs_namespace.Namespace:
                A container for
                [services][google.cloud.servicedirectory.v1beta1.Service].
                Namespaces allow administrators to group services
                together and define permissions for a collection of
                services.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, namespace, namespace_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.CreateNamespaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if namespace is not None:
            request.namespace = namespace
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if namespace_id is not None:
            request.namespace_id = namespace_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_namespace,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_namespaces(
        self,
        request: registration_service.ListNamespacesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNamespacesPager:
        r"""Lists all namespaces.

        Args:
            request (:class:`~.registration_service.ListNamespacesRequest`):
                The request object. The request message for
                [RegistrationService.ListNamespaces][google.cloud.servicedirectory.v1beta1.RegistrationService.ListNamespaces].
            parent (:class:`str`):
                Required. The resource name of the
                project and location whose namespaces
                we'd like to list.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListNamespacesPager:
                The response message for
                [RegistrationService.ListNamespaces][google.cloud.servicedirectory.v1beta1.RegistrationService.ListNamespaces].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.ListNamespacesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_namespaces,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListNamespacesPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def get_namespace(
        self,
        request: registration_service.GetNamespaceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> namespace.Namespace:
        r"""Gets a namespace.

        Args:
            request (:class:`~.registration_service.GetNamespaceRequest`):
                The request object. The request message for
                [RegistrationService.GetNamespace][google.cloud.servicedirectory.v1beta1.RegistrationService.GetNamespace].
            name (:class:`str`):
                Required. The name of the namespace
                to retrieve.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.namespace.Namespace:
                A container for
                [services][google.cloud.servicedirectory.v1beta1.Service].
                Namespaces allow administrators to group services
                together and define permissions for a collection of
                services.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.GetNamespaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_namespace,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def update_namespace(
        self,
        request: registration_service.UpdateNamespaceRequest = None,
        *,
        namespace: gcs_namespace.Namespace = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcs_namespace.Namespace:
        r"""Updates a namespace.

        Args:
            request (:class:`~.registration_service.UpdateNamespaceRequest`):
                The request object. The request message for
                [RegistrationService.UpdateNamespace][google.cloud.servicedirectory.v1beta1.RegistrationService.UpdateNamespace].
            namespace (:class:`~.gcs_namespace.Namespace`):
                Required. The updated namespace.
                This corresponds to the ``namespace`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Required. List of fields to be
                updated in this request.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcs_namespace.Namespace:
                A container for
                [services][google.cloud.servicedirectory.v1beta1.Service].
                Namespaces allow administrators to group services
                together and define permissions for a collection of
                services.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([namespace, update_mask]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.UpdateNamespaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if namespace is not None:
            request.namespace = namespace
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_namespace,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def delete_namespace(
        self,
        request: registration_service.DeleteNamespaceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a namespace. This also deletes all services
        and endpoints in the namespace.

        Args:
            request (:class:`~.registration_service.DeleteNamespaceRequest`):
                The request object. The request message for
                [RegistrationService.DeleteNamespace][google.cloud.servicedirectory.v1beta1.RegistrationService.DeleteNamespace].
            name (:class:`str`):
                Required. The name of the namespace
                to delete.
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
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.DeleteNamespaceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_namespace,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def create_service(
        self,
        request: registration_service.CreateServiceRequest = None,
        *,
        parent: str = None,
        service: gcs_service.Service = None,
        service_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcs_service.Service:
        r"""Creates a service, and returns the new Service.

        Args:
            request (:class:`~.registration_service.CreateServiceRequest`):
                The request object. The request message for
                [RegistrationService.CreateService][google.cloud.servicedirectory.v1beta1.RegistrationService.CreateService].
            parent (:class:`str`):
                Required. The resource name of the
                namespace this service will belong to.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service (:class:`~.gcs_service.Service`):
                Required. A service  with initial
                fields set.
                This corresponds to the ``service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            service_id (:class:`str`):
                Required. The Resource ID must be 1-63 characters long,
                and comply with RFC1035. Specifically, the name must be
                1-63 characters long and match the regular expression
                ``[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?`` which means the
                first character must be a lowercase letter, and all
                following characters must be a dash, lowercase letter,
                or digit, except the last character, which cannot be a
                dash.
                This corresponds to the ``service_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcs_service.Service:
                An individual service. A service contains a name and
                optional metadata. A service must exist before
                [endpoints][google.cloud.servicedirectory.v1beta1.Endpoint]
                can be added to it.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, service, service_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.CreateServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service is not None:
            request.service = service
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service_id is not None:
            request.service_id = service_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_service,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_services(
        self,
        request: registration_service.ListServicesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListServicesPager:
        r"""Lists all services belonging to a namespace.

        Args:
            request (:class:`~.registration_service.ListServicesRequest`):
                The request object. The request message for
                [RegistrationService.ListServices][google.cloud.servicedirectory.v1beta1.RegistrationService.ListServices].
            parent (:class:`str`):
                Required. The resource name of the
                namespace whose services we'd like to
                list.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListServicesPager:
                The response message for
                [RegistrationService.ListServices][google.cloud.servicedirectory.v1beta1.RegistrationService.ListServices].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.ListServicesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_services,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListServicesPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def get_service(
        self,
        request: registration_service.GetServiceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> service.Service:
        r"""Gets a service.

        Args:
            request (:class:`~.registration_service.GetServiceRequest`):
                The request object. The request message for
                [RegistrationService.GetService][google.cloud.servicedirectory.v1beta1.RegistrationService.GetService].
                This should not be used for looking up a service.
                Insead, use the `resolve` method as it will contain all
                endpoints and associated metadata.
            name (:class:`str`):
                Required. The name of the service to
                get.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.service.Service:
                An individual service. A service contains a name and
                optional metadata. A service must exist before
                [endpoints][google.cloud.servicedirectory.v1beta1.Endpoint]
                can be added to it.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.GetServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_service, default_timeout=None, client_info=_client_info
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def update_service(
        self,
        request: registration_service.UpdateServiceRequest = None,
        *,
        service: gcs_service.Service = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcs_service.Service:
        r"""Updates a service.

        Args:
            request (:class:`~.registration_service.UpdateServiceRequest`):
                The request object. The request message for
                [RegistrationService.UpdateService][google.cloud.servicedirectory.v1beta1.RegistrationService.UpdateService].
            service (:class:`~.gcs_service.Service`):
                Required. The updated service.
                This corresponds to the ``service`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Required. List of fields to be
                updated in this request.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcs_service.Service:
                An individual service. A service contains a name and
                optional metadata. A service must exist before
                [endpoints][google.cloud.servicedirectory.v1beta1.Endpoint]
                can be added to it.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([service, update_mask]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.UpdateServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if service is not None:
            request.service = service
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_service,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def delete_service(
        self,
        request: registration_service.DeleteServiceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a service. This also deletes all endpoints
        associated with the service.

        Args:
            request (:class:`~.registration_service.DeleteServiceRequest`):
                The request object. The request message for
                [RegistrationService.DeleteService][google.cloud.servicedirectory.v1beta1.RegistrationService.DeleteService].
            name (:class:`str`):
                Required. The name of the service to
                delete.
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
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.DeleteServiceRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_service,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def create_endpoint(
        self,
        request: registration_service.CreateEndpointRequest = None,
        *,
        parent: str = None,
        endpoint: gcs_endpoint.Endpoint = None,
        endpoint_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcs_endpoint.Endpoint:
        r"""Creates a endpoint, and returns the new Endpoint.

        Args:
            request (:class:`~.registration_service.CreateEndpointRequest`):
                The request object. The request message for
                [RegistrationService.CreateEndpoint][google.cloud.servicedirectory.v1beta1.RegistrationService.CreateEndpoint].
            parent (:class:`str`):
                Required. The resource name of the
                service that this endpoint provides.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            endpoint (:class:`~.gcs_endpoint.Endpoint`):
                Required. A endpoint with initial
                fields set.
                This corresponds to the ``endpoint`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            endpoint_id (:class:`str`):
                Required. The Resource ID must be 1-63 characters long,
                and comply with RFC1035. Specifically, the name must be
                1-63 characters long and match the regular expression
                ``[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?`` which means the
                first character must be a lowercase letter, and all
                following characters must be a dash, lowercase letter,
                or digit, except the last character, which cannot be a
                dash.
                This corresponds to the ``endpoint_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcs_endpoint.Endpoint:
                An individual endpoint that provides a
                [service][google.cloud.servicedirectory.v1beta1.Service].
                The service must already exist to create an endpoint.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, endpoint, endpoint_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.CreateEndpointRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if endpoint is not None:
            request.endpoint = endpoint
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if endpoint_id is not None:
            request.endpoint_id = endpoint_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_endpoint,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_endpoints(
        self,
        request: registration_service.ListEndpointsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListEndpointsPager:
        r"""Lists all endpoints.

        Args:
            request (:class:`~.registration_service.ListEndpointsRequest`):
                The request object. The request message for
                [RegistrationService.ListEndpoints][google.cloud.servicedirectory.v1beta1.RegistrationService.ListEndpoints].
            parent (:class:`str`):
                Required. The resource name of the
                service whose endpoints we'd like to
                list.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListEndpointsPager:
                The response message for
                [RegistrationService.ListEndpoints][google.cloud.servicedirectory.v1beta1.RegistrationService.ListEndpoints].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.ListEndpointsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_endpoints,
            default_timeout=None,
            client_info=_client_info,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListEndpointsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def get_endpoint(
        self,
        request: registration_service.GetEndpointRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> endpoint.Endpoint:
        r"""Gets a endpoint.

        Args:
            request (:class:`~.registration_service.GetEndpointRequest`):
                The request object. The request message for
                [RegistrationService.GetEndpoint][google.cloud.servicedirectory.v1beta1.RegistrationService.GetEndpoint].
                This should not be used to lookup endpoints at runtime.
                Instead, use the `resolve` method.
            name (:class:`str`):
                Required. The name of the endpoint to
                get.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.endpoint.Endpoint:
                An individual endpoint that provides a
                [service][google.cloud.servicedirectory.v1beta1.Service].
                The service must already exist to create an endpoint.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.GetEndpointRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_endpoint, default_timeout=None, client_info=_client_info
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def update_endpoint(
        self,
        request: registration_service.UpdateEndpointRequest = None,
        *,
        endpoint: gcs_endpoint.Endpoint = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcs_endpoint.Endpoint:
        r"""Updates a endpoint.

        Args:
            request (:class:`~.registration_service.UpdateEndpointRequest`):
                The request object. The request message for
                [RegistrationService.UpdateEndpoint][google.cloud.servicedirectory.v1beta1.RegistrationService.UpdateEndpoint].
            endpoint (:class:`~.gcs_endpoint.Endpoint`):
                Required. The updated endpoint.
                This corresponds to the ``endpoint`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Required. List of fields to be
                updated in this request.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcs_endpoint.Endpoint:
                An individual endpoint that provides a
                [service][google.cloud.servicedirectory.v1beta1.Service].
                The service must already exist to create an endpoint.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([endpoint, update_mask]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.UpdateEndpointRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if endpoint is not None:
            request.endpoint = endpoint
        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_endpoint,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def delete_endpoint(
        self,
        request: registration_service.DeleteEndpointRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a endpoint.

        Args:
            request (:class:`~.registration_service.DeleteEndpointRequest`):
                The request object. The request message for
                [RegistrationService.DeleteEndpoint][google.cloud.servicedirectory.v1beta1.RegistrationService.DeleteEndpoint].
            name (:class:`str`):
                Required. The name of the endpoint to
                delete.
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
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = registration_service.DeleteEndpointRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_endpoint,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def get_iam_policy(
        self,
        request: iam_policy.GetIamPolicyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy.Policy:
        r"""Gets the IAM Policy for a resource (namespace or
        service only).

        Args:
            request (:class:`~.iam_policy.GetIamPolicyRequest`):
                The request object. Request message for `GetIamPolicy`
                method.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.policy.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.

                A ``Policy`` consists of a list of ``bindings``. A
                ``Binding`` binds a list of ``members`` to a ``role``,
                where the members can be user accounts, Google groups,
                Google domains, and service accounts. A ``role`` is a
                named list of permissions defined by IAM.

                **Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/owner",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-other-app@appspot.gserviceaccount.com",
                          ]
                        },
                        {
                          "role": "roles/viewer",
                          "members": ["user:sean@example.com"]
                        }
                      ]
                    }

                For a description of IAM and its features, see the `IAM
                developer's guide <https://cloud.google.com/iam>`__.

        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy.GetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_iam_policy,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: iam_policy.SetIamPolicyRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy.Policy:
        r"""Sets the IAM Policy for a resource (namespace or
        service only).

        Args:
            request (:class:`~.iam_policy.SetIamPolicyRequest`):
                The request object. Request message for `SetIamPolicy`
                method.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.policy.Policy:
                Defines an Identity and Access Management (IAM) policy.
                It is used to specify access control policies for Cloud
                Platform resources.

                A ``Policy`` consists of a list of ``bindings``. A
                ``Binding`` binds a list of ``members`` to a ``role``,
                where the members can be user accounts, Google groups,
                Google domains, and service accounts. A ``role`` is a
                named list of permissions defined by IAM.

                **Example**

                ::

                    {
                      "bindings": [
                        {
                          "role": "roles/owner",
                          "members": [
                            "user:mike@example.com",
                            "group:admins@example.com",
                            "domain:google.com",
                            "serviceAccount:my-other-app@appspot.gserviceaccount.com",
                          ]
                        },
                        {
                          "role": "roles/viewer",
                          "members": ["user:sean@example.com"]
                        }
                      ]
                    }

                For a description of IAM and its features, see the `IAM
                developer's guide <https://cloud.google.com/iam>`__.

        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy.SetIamPolicyRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.set_iam_policy,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def test_iam_permissions(
        self,
        request: iam_policy.TestIamPermissionsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy.TestIamPermissionsResponse:
        r"""Tests IAM permissions for a resource (namespace or
        service only).

        Args:
            request (:class:`~.iam_policy.TestIamPermissionsRequest`):
                The request object. Request message for
                `TestIamPermissions` method.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.iam_policy.TestIamPermissionsResponse:
                Response message for ``TestIamPermissions`` method.
        """
        # Create or coerce a protobuf request object.

        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = iam_policy.TestIamPermissionsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.test_iam_permissions,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-service-directory"
        ).version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("RegistrationServiceClient",)
