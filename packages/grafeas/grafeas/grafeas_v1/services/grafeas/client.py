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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from grafeas.grafeas_v1.services.grafeas import pagers
from grafeas.grafeas_v1.types import attestation
from grafeas.grafeas_v1.types import build
from grafeas.grafeas_v1.types import common
from grafeas.grafeas_v1.types import compliance
from grafeas.grafeas_v1.types import deployment
from grafeas.grafeas_v1.types import discovery
from grafeas.grafeas_v1.types import dsse_attestation
from grafeas.grafeas_v1.types import grafeas
from grafeas.grafeas_v1.types import image
from grafeas.grafeas_v1.types import package
from grafeas.grafeas_v1.types import upgrade
from grafeas.grafeas_v1.types import vulnerability
from .transports.base import GrafeasTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import GrafeasGrpcTransport
from .transports.grpc_asyncio import GrafeasGrpcAsyncIOTransport


class GrafeasClientMeta(type):
    """Metaclass for the Grafeas client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[GrafeasTransport]]
    _transport_registry["grpc"] = GrafeasGrpcTransport
    _transport_registry["grpc_asyncio"] = GrafeasGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[GrafeasTransport]:
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


class GrafeasClient(metaclass=GrafeasClientMeta):
    """`Grafeas <https://grafeas.io>`__ API.

    Retrieves analysis results of Cloud components such as Docker
    container images.

    Analysis results are stored as a series of occurrences. An
    ``Occurrence`` contains information about a specific analysis
    instance on a resource. An occurrence refers to a ``Note``. A note
    contains details describing the analysis and is generally stored in
    a separate project, called a ``Provider``. Multiple occurrences can
    refer to the same note.

    For example, an SSL vulnerability could affect multiple images. In
    this case, there would be one note for the vulnerability and an
    occurrence for each image with the vulnerability referring to that
    note.
    """

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

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            GrafeasClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @property
    def transport(self) -> GrafeasTransport:
        """Returns the transport used by the client instance.

        Returns:
            GrafeasTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def note_path(project: str, note: str,) -> str:
        """Returns a fully-qualified note string."""
        return "projects/{project}/notes/{note}".format(project=project, note=note,)

    @staticmethod
    def parse_note_path(path: str) -> Dict[str, str]:
        """Parses a note path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/notes/(?P<note>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def occurrence_path(project: str, occurrence: str,) -> str:
        """Returns a fully-qualified occurrence string."""
        return "projects/{project}/occurrences/{occurrence}".format(
            project=project, occurrence=occurrence,
        )

    @staticmethod
    def parse_occurrence_path(path: str) -> Dict[str, str]:
        """Parses a occurrence path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/occurrences/(?P<occurrence>.+?)$", path
        )
        return m.groupdict() if m else {}

    @staticmethod
    def project_path(project: str,) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(project=project,)

    @staticmethod
    def parse_project_path(path: str) -> Dict[str, str]:
        """Parses a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
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

    def __init__(self, *, transport: Union[str, GrafeasTransport] = None,) -> None:
        """Instantiate the grafeas client.

        Args:
            transport (Union[str, ~.GrafeasTransport]): The
                transport to use.
            

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        if isinstance(transport, GrafeasTransport):
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport()

    def get_occurrence(
        self,
        request: Union[grafeas.GetOccurrenceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Occurrence:
        r"""Gets the specified occurrence.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_get_occurrence():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.GetOccurrenceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_occurrence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.GetOccurrenceRequest, dict]):
                The request object. Request to get an occurrence.
            name (str):
                The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Occurrence:
                An instance of an analysis type that
                has been found on a resource.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.GetOccurrenceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.GetOccurrenceRequest):
            request = grafeas.GetOccurrenceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_occurrence]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_occurrences(
        self,
        request: Union[grafeas.ListOccurrencesRequest, dict] = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListOccurrencesPager:
        r"""Lists occurrences for the specified project.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_list_occurrences():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.ListOccurrencesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_occurrences(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.ListOccurrencesRequest, dict]):
                The request object. Request to list occurrences.
            parent (str):
                The name of the project to list occurrences for in the
                form of ``projects/[PROJECT_ID]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                The filter expression.
                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.services.grafeas.pagers.ListOccurrencesPager:
                Response for listing occurrences.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.ListOccurrencesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.ListOccurrencesRequest):
            request = grafeas.ListOccurrencesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_occurrences]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListOccurrencesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_occurrence(
        self,
        request: Union[grafeas.DeleteOccurrenceRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified occurrence. For example, use
        this method to delete an occurrence when the occurrence
        is no longer applicable for the given resource.


        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_delete_occurrence():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.DeleteOccurrenceRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_occurrence(request=request)

        Args:
            request (Union[grafeas.grafeas_v1.types.DeleteOccurrenceRequest, dict]):
                The request object. Request to delete an occurrence.
            name (str):
                The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.DeleteOccurrenceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.DeleteOccurrenceRequest):
            request = grafeas.DeleteOccurrenceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_occurrence]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def create_occurrence(
        self,
        request: Union[grafeas.CreateOccurrenceRequest, dict] = None,
        *,
        parent: str = None,
        occurrence: grafeas.Occurrence = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Occurrence:
        r"""Creates a new occurrence.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_create_occurrence():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.CreateOccurrenceRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.create_occurrence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.CreateOccurrenceRequest, dict]):
                The request object. Request to create a new occurrence.
            parent (str):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the occurrence is
                to be created.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            occurrence (grafeas.grafeas_v1.types.Occurrence):
                The occurrence to create.
                This corresponds to the ``occurrence`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Occurrence:
                An instance of an analysis type that
                has been found on a resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, occurrence])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.CreateOccurrenceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.CreateOccurrenceRequest):
            request = grafeas.CreateOccurrenceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if occurrence is not None:
                request.occurrence = occurrence

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_occurrence]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_create_occurrences(
        self,
        request: Union[grafeas.BatchCreateOccurrencesRequest, dict] = None,
        *,
        parent: str = None,
        occurrences: Sequence[grafeas.Occurrence] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.BatchCreateOccurrencesResponse:
        r"""Creates new occurrences in batch.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_batch_create_occurrences():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.BatchCreateOccurrencesRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.batch_create_occurrences(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.BatchCreateOccurrencesRequest, dict]):
                The request object. Request to create occurrences in
                batch.
            parent (str):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the occurrences
                are to be created.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            occurrences (Sequence[grafeas.grafeas_v1.types.Occurrence]):
                The occurrences to create. Max
                allowed length is 1000.

                This corresponds to the ``occurrences`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.BatchCreateOccurrencesResponse:
                Response for creating occurrences in
                batch.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, occurrences])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.BatchCreateOccurrencesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.BatchCreateOccurrencesRequest):
            request = grafeas.BatchCreateOccurrencesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if occurrences is not None:
                request.occurrences = occurrences

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_create_occurrences]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_occurrence(
        self,
        request: Union[grafeas.UpdateOccurrenceRequest, dict] = None,
        *,
        name: str = None,
        occurrence: grafeas.Occurrence = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Occurrence:
        r"""Updates the specified occurrence.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_update_occurrence():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.UpdateOccurrenceRequest(
                    name="name_value",
                )

                # Make the request
                response = client.update_occurrence(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.UpdateOccurrenceRequest, dict]):
                The request object. Request to update an occurrence.
            name (str):
                The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            occurrence (grafeas.grafeas_v1.types.Occurrence):
                The updated occurrence.
                This corresponds to the ``occurrence`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The fields to update.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Occurrence:
                An instance of an analysis type that
                has been found on a resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, occurrence, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.UpdateOccurrenceRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.UpdateOccurrenceRequest):
            request = grafeas.UpdateOccurrenceRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if occurrence is not None:
                request.occurrence = occurrence
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_occurrence]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_occurrence_note(
        self,
        request: Union[grafeas.GetOccurrenceNoteRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Note:
        r"""Gets the note attached to the specified occurrence.
        Consumer projects can use this method to get a note that
        belongs to a provider project.


        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_get_occurrence_note():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.GetOccurrenceNoteRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_occurrence_note(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.GetOccurrenceNoteRequest, dict]):
                The request object. Request to get the note to which the
                specified occurrence is attached.
            name (str):
                The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Note:
                A type of analysis that can be done
                for a resource.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.GetOccurrenceNoteRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.GetOccurrenceNoteRequest):
            request = grafeas.GetOccurrenceNoteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_occurrence_note]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_note(
        self,
        request: Union[grafeas.GetNoteRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Note:
        r"""Gets the specified note.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_get_note():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.GetNoteRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_note(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.GetNoteRequest, dict]):
                The request object. Request to get a note.
            name (str):
                The name of the note in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Note:
                A type of analysis that can be done
                for a resource.

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

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.GetNoteRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.GetNoteRequest):
            request = grafeas.GetNoteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_note]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_notes(
        self,
        request: Union[grafeas.ListNotesRequest, dict] = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNotesPager:
        r"""Lists notes for the specified project.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_list_notes():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.ListNotesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_notes(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.ListNotesRequest, dict]):
                The request object. Request to list notes.
            parent (str):
                The name of the project to list notes for in the form of
                ``projects/[PROJECT_ID]``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                The filter expression.
                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.services.grafeas.pagers.ListNotesPager:
                Response for listing notes.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.ListNotesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.ListNotesRequest):
            request = grafeas.ListNotesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_notes]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListNotesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_note(
        self,
        request: Union[grafeas.DeleteNoteRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified note.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_delete_note():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.DeleteNoteRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_note(request=request)

        Args:
            request (Union[grafeas.grafeas_v1.types.DeleteNoteRequest, dict]):
                The request object. Request to delete a note.
            name (str):
                The name of the note in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.

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
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.DeleteNoteRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.DeleteNoteRequest):
            request = grafeas.DeleteNoteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_note]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def create_note(
        self,
        request: Union[grafeas.CreateNoteRequest, dict] = None,
        *,
        parent: str = None,
        note_id: str = None,
        note: grafeas.Note = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Note:
        r"""Creates a new note.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_create_note():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.CreateNoteRequest(
                    parent="parent_value",
                    note_id="note_id_value",
                )

                # Make the request
                response = client.create_note(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.CreateNoteRequest, dict]):
                The request object. Request to create a new note.
            parent (str):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the note is to be
                created.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            note_id (str):
                The ID to use for this note.
                This corresponds to the ``note_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            note (grafeas.grafeas_v1.types.Note):
                The note to create.
                This corresponds to the ``note`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Note:
                A type of analysis that can be done
                for a resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, note_id, note])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.CreateNoteRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.CreateNoteRequest):
            request = grafeas.CreateNoteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if note_id is not None:
                request.note_id = note_id
            if note is not None:
                request.note = note

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_note]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def batch_create_notes(
        self,
        request: Union[grafeas.BatchCreateNotesRequest, dict] = None,
        *,
        parent: str = None,
        notes: Sequence[grafeas.BatchCreateNotesRequest.NotesEntry] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.BatchCreateNotesResponse:
        r"""Creates new notes in batch.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_batch_create_notes():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.BatchCreateNotesRequest(
                    parent="parent_value",
                )

                # Make the request
                response = client.batch_create_notes(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.BatchCreateNotesRequest, dict]):
                The request object. Request to create notes in batch.
            parent (str):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the notes are to
                be created.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            notes (Sequence[grafeas.grafeas_v1.types.BatchCreateNotesRequest.NotesEntry]):
                The notes to create. Max allowed
                length is 1000.

                This corresponds to the ``notes`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.BatchCreateNotesResponse:
                Response for creating notes in batch.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, notes])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.BatchCreateNotesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.BatchCreateNotesRequest):
            request = grafeas.BatchCreateNotesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if notes is not None:
                request.notes = notes

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.batch_create_notes]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_note(
        self,
        request: Union[grafeas.UpdateNoteRequest, dict] = None,
        *,
        name: str = None,
        note: grafeas.Note = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Note:
        r"""Updates the specified note.

        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_update_note():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.UpdateNoteRequest(
                    name="name_value",
                )

                # Make the request
                response = client.update_note(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.UpdateNoteRequest, dict]):
                The request object. Request to update a note.
            name (str):
                The name of the note in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            note (grafeas.grafeas_v1.types.Note):
                The updated note.
                This corresponds to the ``note`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                The fields to update.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.types.Note:
                A type of analysis that can be done
                for a resource.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, note, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.UpdateNoteRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.UpdateNoteRequest):
            request = grafeas.UpdateNoteRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if note is not None:
                request.note = note
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_note]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_note_occurrences(
        self,
        request: Union[grafeas.ListNoteOccurrencesRequest, dict] = None,
        *,
        name: str = None,
        filter: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNoteOccurrencesPager:
        r"""Lists occurrences referencing the specified note.
        Provider projects can use this method to get all
        occurrences across consumer projects referencing the
        specified note.


        .. code-block:: python

            from grafeas import grafeas_v1

            def sample_list_note_occurrences():
                # Create a client
                client = grafeas_v1.GrafeasClient()

                # Initialize request argument(s)
                request = grafeas_v1.ListNoteOccurrencesRequest(
                    name="name_value",
                )

                # Make the request
                page_result = client.list_note_occurrences(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[grafeas.grafeas_v1.types.ListNoteOccurrencesRequest, dict]):
                The request object. Request to list occurrences for a
                note.
            name (str):
                The name of the note to list occurrences for in the form
                of ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (str):
                The filter expression.
                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            grafeas.grafeas_v1.services.grafeas.pagers.ListNoteOccurrencesPager:
                Response for listing occurrences for
                a note.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, filter])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a grafeas.ListNoteOccurrencesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, grafeas.ListNoteOccurrencesRequest):
            request = grafeas.ListNoteOccurrencesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name
            if filter is not None:
                request.filter = filter

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_note_occurrences]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListNoteOccurrencesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

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
        gapic_version=pkg_resources.get_distribution("grafeas",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("GrafeasClient",)
