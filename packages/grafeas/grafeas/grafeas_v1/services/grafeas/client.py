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

from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from grafeas.grafeas_v1.services.grafeas import pagers
from grafeas.grafeas_v1.types import attestation
from grafeas.grafeas_v1.types import build
from grafeas.grafeas_v1.types import common
from grafeas.grafeas_v1.types import deployment
from grafeas.grafeas_v1.types import discovery
from grafeas.grafeas_v1.types import grafeas
from grafeas.grafeas_v1.types import image
from grafeas.grafeas_v1.types import package
from grafeas.grafeas_v1.types import upgrade
from grafeas.grafeas_v1.types import vulnerability

from .transports.base import GrafeasTransport
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

    DEFAULT_ENDPOINT = "containeranalysis.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @staticmethod
    def note_path(project: str, note: str,) -> str:
        """Return a fully-qualified note string."""
        return "projects/{project}/notes/{note}".format(project=project, note=note,)

    @staticmethod
    def parse_note_path(path: str) -> Dict[str, str]:
        """Parse a note path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/notes/(?P<note>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def occurrence_path(project: str, occurrence: str,) -> str:
        """Return a fully-qualified occurrence string."""
        return "projects/{project}/occurrences/{occurrence}".format(
            project=project, occurrence=occurrence,
        )

    @staticmethod
    def parse_occurrence_path(path: str) -> Dict[str, str]:
        """Parse a occurrence path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/occurrences/(?P<occurrence>.+?)$", path
        )
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
        request: grafeas.GetOccurrenceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Occurrence:
        r"""Gets the specified occurrence.

        Args:
            request (:class:`~.grafeas.GetOccurrenceRequest`):
                The request object. Request to get an occurrence.
            name (:class:`str`):
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
            ~.grafeas.Occurrence:
                An instance of an analysis type that
                has been found on a resource.

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
        request: grafeas.ListOccurrencesRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListOccurrencesPager:
        r"""Lists occurrences for the specified project.

        Args:
            request (:class:`~.grafeas.ListOccurrencesRequest`):
                The request object. Request to list occurrences.
            parent (:class:`str`):
                The name of the project to list occurrences for in the
                form of ``projects/[PROJECT_ID]``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
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
            ~.pagers.ListOccurrencesPager:
                Response for listing occurrences.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
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
        request: grafeas.DeleteOccurrenceRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified occurrence. For example, use
        this method to delete an occurrence when the occurrence
        is no longer applicable for the given resource.

        Args:
            request (:class:`~.grafeas.DeleteOccurrenceRequest`):
                The request object. Request to delete an occurrence.
            name (:class:`str`):
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
        # Sanity check: If we got a request object, we should *not* have
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
        request: grafeas.CreateOccurrenceRequest = None,
        *,
        parent: str = None,
        occurrence: grafeas.Occurrence = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Occurrence:
        r"""Creates a new occurrence.

        Args:
            request (:class:`~.grafeas.CreateOccurrenceRequest`):
                The request object. Request to create a new occurrence.
            parent (:class:`str`):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the occurrence is
                to be created.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            occurrence (:class:`~.grafeas.Occurrence`):
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
            ~.grafeas.Occurrence:
                An instance of an analysis type that
                has been found on a resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
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
        request: grafeas.BatchCreateOccurrencesRequest = None,
        *,
        parent: str = None,
        occurrences: Sequence[grafeas.Occurrence] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.BatchCreateOccurrencesResponse:
        r"""Creates new occurrences in batch.

        Args:
            request (:class:`~.grafeas.BatchCreateOccurrencesRequest`):
                The request object. Request to create occurrences in
                batch.
            parent (:class:`str`):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the occurrences
                are to be created.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            occurrences (:class:`Sequence[~.grafeas.Occurrence]`):
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
            ~.grafeas.BatchCreateOccurrencesResponse:
                Response for creating occurrences in
                batch.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
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
        request: grafeas.UpdateOccurrenceRequest = None,
        *,
        name: str = None,
        occurrence: grafeas.Occurrence = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Occurrence:
        r"""Updates the specified occurrence.

        Args:
            request (:class:`~.grafeas.UpdateOccurrenceRequest`):
                The request object. Request to update an occurrence.
            name (:class:`str`):
                The name of the occurrence in the form of
                ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            occurrence (:class:`~.grafeas.Occurrence`):
                The updated occurrence.
                This corresponds to the ``occurrence`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
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
            ~.grafeas.Occurrence:
                An instance of an analysis type that
                has been found on a resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
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
        request: grafeas.GetOccurrenceNoteRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Note:
        r"""Gets the note attached to the specified occurrence.
        Consumer projects can use this method to get a note that
        belongs to a provider project.

        Args:
            request (:class:`~.grafeas.GetOccurrenceNoteRequest`):
                The request object. Request to get the note to which the
                specified occurrence is attached.
            name (:class:`str`):
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
            ~.grafeas.Note:
                A type of analysis that can be done
                for a resource.

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
        request: grafeas.GetNoteRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Note:
        r"""Gets the specified note.

        Args:
            request (:class:`~.grafeas.GetNoteRequest`):
                The request object. Request to get a note.
            name (:class:`str`):
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
            ~.grafeas.Note:
                A type of analysis that can be done
                for a resource.

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
        request: grafeas.ListNotesRequest = None,
        *,
        parent: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNotesPager:
        r"""Lists notes for the specified project.

        Args:
            request (:class:`~.grafeas.ListNotesRequest`):
                The request object. Request to list notes.
            parent (:class:`str`):
                The name of the project to list notes for in the form of
                ``projects/[PROJECT_ID]``.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
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
            ~.pagers.ListNotesPager:
                Response for listing notes.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
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
        request: grafeas.DeleteNoteRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes the specified note.

        Args:
            request (:class:`~.grafeas.DeleteNoteRequest`):
                The request object. Request to delete a note.
            name (:class:`str`):
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
        # Sanity check: If we got a request object, we should *not* have
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
        request: grafeas.CreateNoteRequest = None,
        *,
        parent: str = None,
        note_id: str = None,
        note: grafeas.Note = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Note:
        r"""Creates a new note.

        Args:
            request (:class:`~.grafeas.CreateNoteRequest`):
                The request object. Request to create a new note.
            parent (:class:`str`):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the note is to be
                created.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            note_id (:class:`str`):
                The ID to use for this note.
                This corresponds to the ``note_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            note (:class:`~.grafeas.Note`):
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
            ~.grafeas.Note:
                A type of analysis that can be done
                for a resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
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
        request: grafeas.BatchCreateNotesRequest = None,
        *,
        parent: str = None,
        notes: Sequence[grafeas.BatchCreateNotesRequest.NotesEntry] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.BatchCreateNotesResponse:
        r"""Creates new notes in batch.

        Args:
            request (:class:`~.grafeas.BatchCreateNotesRequest`):
                The request object. Request to create notes in batch.
            parent (:class:`str`):
                The name of the project in the form of
                ``projects/[PROJECT_ID]``, under which the notes are to
                be created.
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            notes (:class:`Sequence[~.grafeas.BatchCreateNotesRequest.NotesEntry]`):
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
            ~.grafeas.BatchCreateNotesResponse:
                Response for creating notes in batch.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
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
        request: grafeas.UpdateNoteRequest = None,
        *,
        name: str = None,
        note: grafeas.Note = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> grafeas.Note:
        r"""Updates the specified note.

        Args:
            request (:class:`~.grafeas.UpdateNoteRequest`):
                The request object. Request to update a note.
            name (:class:`str`):
                The name of the note in the form of
                ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            note (:class:`~.grafeas.Note`):
                The updated note.
                This corresponds to the ``note`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
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
            ~.grafeas.Note:
                A type of analysis that can be done
                for a resource.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
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
        request: grafeas.ListNoteOccurrencesRequest = None,
        *,
        name: str = None,
        filter: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListNoteOccurrencesPager:
        r"""Lists occurrences referencing the specified note.
        Provider projects can use this method to get all
        occurrences across consumer projects referencing the
        specified note.

        Args:
            request (:class:`~.grafeas.ListNoteOccurrencesRequest`):
                The request object. Request to list occurrences for a
                note.
            name (:class:`str`):
                The name of the note to list occurrences for in the form
                of ``projects/[PROVIDER_ID]/notes/[NOTE_ID]``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
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
            ~.pagers.ListNoteOccurrencesPager:
                Response for listing occurrences for
                a note.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
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


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("grafeas",).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("GrafeasClient",)
