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
import re
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.bigquery.reservation_v1.services.reservation_service import pagers
from google.cloud.bigquery.reservation_v1.types import reservation
from google.cloud.bigquery.reservation_v1.types import reservation as gcbr_reservation
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore

from .transports.base import ReservationServiceTransport
from .transports.grpc import ReservationServiceGrpcTransport


class ReservationServiceClientMeta(type):
    """Metaclass for the ReservationService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = (
        OrderedDict()
    )  # type: Dict[str, Type[ReservationServiceTransport]]
    _transport_registry["grpc"] = ReservationServiceGrpcTransport

    def get_transport_class(
        cls, label: str = None
    ) -> Type[ReservationServiceTransport]:
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


class ReservationServiceClient(metaclass=ReservationServiceClientMeta):
    """This API allows users to manage their flat-rate BigQuery
    reservations.

    A reservation provides computational resource guarantees, in the
    form of `slots <https://cloud.google.com/bigquery/docs/slots>`__, to
    users. A slot is a unit of computational power in BigQuery, and
    serves as the basic unit of parallelism. In a scan of a
    multi-partitioned table, a single slot operates on a single
    partition of the table. A reservation resource exists as a child
    resource of the admin project and location, e.g.:
    ``projects/myproject/locations/US/reservations/reservationName``.

    A capacity commitment is a way to purchase compute capacity for
    BigQuery jobs (in the form of slots) with some committed period of
    usage. A capacity commitment resource exists as a child resource of
    the admin project and location, e.g.:
    ``projects/myproject/locations/US/capacityCommitments/id``.
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

    DEFAULT_ENDPOINT = "bigqueryreservation.googleapis.com"
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
    def assignment_path(
        project: str, location: str, reservation: str, assignment: str
    ) -> str:
        """Return a fully-qualified assignment string."""
        return "projects/{project}/locations/{location}/reservations/{reservation}/assignments/{assignment}".format(
            project=project,
            location=location,
            reservation=reservation,
            assignment=assignment,
        )

    @staticmethod
    def parse_assignment_path(path: str) -> Dict[str, str]:
        """Parse a assignment path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/reservations/(?P<reservation>.+?)/assignments/(?P<assignment>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def reservation_path(project: str, location: str, reservation: str) -> str:
        """Return a fully-qualified reservation string."""
        return "projects/{project}/locations/{location}/reservations/{reservation}".format(
            project=project, location=location, reservation=reservation
        )

    @staticmethod
    def parse_reservation_path(path: str) -> Dict[str, str]:
        """Parse a reservation path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/reservations/(?P<reservation>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def capacity_commitment_path(
        project: str, location: str, capacity_commitment: str
    ) -> str:
        """Return a fully-qualified capacity_commitment string."""
        return "projects/{project}/locations/{location}/capacityCommitments/{capacity_commitment}".format(
            project=project, location=location, capacity_commitment=capacity_commitment
        )

    @staticmethod
    def parse_capacity_commitment_path(path: str) -> Dict[str, str]:
        """Parse a capacity_commitment path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/capacityCommitments/(?P<capacity_commitment>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def bi_reservation_path(project: str, location: str) -> str:
        """Return a fully-qualified bi_reservation string."""
        return "projects/{project}/locations/{location}/bireservation".format(
            project=project, location=location
        )

    @staticmethod
    def parse_bi_reservation_path(path: str) -> Dict[str, str]:
        """Parse a bi_reservation path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/bireservation$",
            path,
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, ReservationServiceTransport] = None,
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the reservation service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ReservationServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client.
                (2) If ``transport`` argument is None, ``client_options`` can be
                used to create a mutual TLS transport. If ``client_cert_source``
                is provided, mutual TLS transport will be created with the given
                ``api_endpoint`` or the default mTLS endpoint, and the client
                SSL credentials obtained from ``client_cert_source``.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, ReservationServiceTransport):
            # transport is a ReservationServiceTransport instance.
            if credentials:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            self._transport = transport
        elif client_options is None or (
            client_options.api_endpoint is None
            and client_options.client_cert_source is None
        ):
            # Don't trigger mTLS if we get an empty ClientOptions.
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials, host=self.DEFAULT_ENDPOINT
            )
        else:
            # We have a non-empty ClientOptions. If client_cert_source is
            # provided, trigger mTLS with user provided endpoint or the default
            # mTLS endpoint.
            if client_options.client_cert_source:
                api_mtls_endpoint = (
                    client_options.api_endpoint
                    if client_options.api_endpoint
                    else self.DEFAULT_MTLS_ENDPOINT
                )
            else:
                api_mtls_endpoint = None

            api_endpoint = (
                client_options.api_endpoint
                if client_options.api_endpoint
                else self.DEFAULT_ENDPOINT
            )

            self._transport = ReservationServiceGrpcTransport(
                credentials=credentials,
                host=api_endpoint,
                api_mtls_endpoint=api_mtls_endpoint,
                client_cert_source=client_options.client_cert_source,
            )

    def create_reservation(
        self,
        request: gcbr_reservation.CreateReservationRequest = None,
        *,
        parent: str = None,
        reservation: gcbr_reservation.Reservation = None,
        reservation_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcbr_reservation.Reservation:
        r"""Creates a new reservation resource.

        Args:
            request (:class:`~.gcbr_reservation.CreateReservationRequest`):
                The request object. The request for
                [ReservationService.CreateReservation][google.cloud.bigquery.reservation.v1.ReservationService.CreateReservation].
            parent (:class:`str`):
                Required. Project, location. E.g.,
                ``projects/myproject/locations/US``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            reservation (:class:`~.gcbr_reservation.Reservation`):
                Definition of the new reservation to
                create.
                This corresponds to the ``reservation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            reservation_id (:class:`str`):
                The reservation ID. This field must
                only contain lower case alphanumeric
                characters or dash. Max length is 64
                characters.
                This corresponds to the ``reservation_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcbr_reservation.Reservation:
                A reservation is a mechanism used to
                guarantee slots to users.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, reservation, reservation_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcbr_reservation.CreateReservationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent
        if reservation is not None:
            request.reservation = reservation
        if reservation_id is not None:
            request.reservation_id = reservation_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_reservation,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_reservations(
        self,
        request: reservation.ListReservationsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListReservationsPager:
        r"""Lists all the reservations for the project in the
        specified location.

        Args:
            request (:class:`~.reservation.ListReservationsRequest`):
                The request object. The request for
                [ReservationService.ListReservations][google.cloud.bigquery.reservation.v1.ReservationService.ListReservations].
            parent (:class:`str`):
                Required. The parent resource name
                containing project and location, e.g.:
                "projects/myproject/locations/US".
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListReservationsPager:
                The response for
                [ReservationService.ListReservations][google.cloud.bigquery.reservation.v1.ReservationService.ListReservations].

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

        request = reservation.ListReservationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_reservations,
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
        response = pagers.ListReservationsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def get_reservation(
        self,
        request: reservation.GetReservationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.Reservation:
        r"""Returns information about the reservation.

        Args:
            request (:class:`~.reservation.GetReservationRequest`):
                The request object. The request for
                [ReservationService.GetReservation][google.cloud.bigquery.reservation.v1.ReservationService.GetReservation].
            name (:class:`str`):
                Required. Resource name of the reservation to retrieve.
                E.g.,
                ``projects/myproject/locations/US/reservations/team1-prod``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.reservation.Reservation:
                A reservation is a mechanism used to
                guarantee slots to users.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.GetReservationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_reservation,
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

    def delete_reservation(
        self,
        request: reservation.DeleteReservationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a reservation. Returns
        ``google.rpc.Code.FAILED_PRECONDITION`` when reservation has
        assignments.

        Args:
            request (:class:`~.reservation.DeleteReservationRequest`):
                The request object. The request for
                [ReservationService.DeleteReservation][google.cloud.bigquery.reservation.v1.ReservationService.DeleteReservation].
            name (:class:`str`):
                Required. Resource name of the reservation to retrieve.
                E.g.,
                ``projects/myproject/locations/US/reservations/team1-prod``
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

        request = reservation.DeleteReservationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_reservation,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def update_reservation(
        self,
        request: gcbr_reservation.UpdateReservationRequest = None,
        *,
        reservation: gcbr_reservation.Reservation = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcbr_reservation.Reservation:
        r"""Updates an existing reservation resource.

        Args:
            request (:class:`~.gcbr_reservation.UpdateReservationRequest`):
                The request object. The request for
                [ReservationService.UpdateReservation][google.cloud.bigquery.reservation.v1.ReservationService.UpdateReservation].
            reservation (:class:`~.gcbr_reservation.Reservation`):
                Content of the reservation to update.
                This corresponds to the ``reservation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Standard field mask for the set of
                fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.gcbr_reservation.Reservation:
                A reservation is a mechanism used to
                guarantee slots to users.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([reservation, update_mask]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = gcbr_reservation.UpdateReservationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if reservation is not None:
            request.reservation = reservation
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_reservation,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def create_capacity_commitment(
        self,
        request: reservation.CreateCapacityCommitmentRequest = None,
        *,
        parent: str = None,
        capacity_commitment: reservation.CapacityCommitment = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.CapacityCommitment:
        r"""Creates a new capacity commitment resource.

        Args:
            request (:class:`~.reservation.CreateCapacityCommitmentRequest`):
                The request object. The request for
                [ReservationService.CreateCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.CreateCapacityCommitment].
            parent (:class:`str`):
                Required. Resource name of the parent
                reservation. E.g.,
                projects/myproject/locations/US
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            capacity_commitment (:class:`~.reservation.CapacityCommitment`):
                Content of the capacity commitment to
                create.
                This corresponds to the ``capacity_commitment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.reservation.CapacityCommitment:
                Capacity commitment is a way to
                purchase compute capacity for BigQuery
                jobs (in the form of slots) with some
                committed period of usage. Annual
                commitments renew by default.
                Commitments can be removed after their
                commitment end time passes.

                In order to remove annual commitment,
                its plan needs to be changed to monthly
                or flex first.

                A capacity commitment resource exists as
                a child resource of the admin project.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, capacity_commitment]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.CreateCapacityCommitmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent
        if capacity_commitment is not None:
            request.capacity_commitment = capacity_commitment

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_capacity_commitment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_capacity_commitments(
        self,
        request: reservation.ListCapacityCommitmentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCapacityCommitmentsPager:
        r"""Lists all the capacity commitments for the admin
        project.

        Args:
            request (:class:`~.reservation.ListCapacityCommitmentsRequest`):
                The request object. The request for
                [ReservationService.ListCapacityCommitments][google.cloud.bigquery.reservation.v1.ReservationService.ListCapacityCommitments].
            parent (:class:`str`):
                Required. Resource name of the parent
                reservation. E.g.,
                projects/myproject/locations/US
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListCapacityCommitmentsPager:
                The response for
                [ReservationService.ListCapacityCommitments][google.cloud.bigquery.reservation.v1.ReservationService.ListCapacityCommitments].

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

        request = reservation.ListCapacityCommitmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_capacity_commitments,
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
        response = pagers.ListCapacityCommitmentsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def get_capacity_commitment(
        self,
        request: reservation.GetCapacityCommitmentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.CapacityCommitment:
        r"""Returns information about the capacity commitment.

        Args:
            request (:class:`~.reservation.GetCapacityCommitmentRequest`):
                The request object. The request for
                [ReservationService.GetCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.GetCapacityCommitment].
            name (:class:`str`):
                Required. Resource name of the
                capacity commitment to retrieve. E.g.,
                projects/myproject/locations/US/capacityCommitments/123
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.reservation.CapacityCommitment:
                Capacity commitment is a way to
                purchase compute capacity for BigQuery
                jobs (in the form of slots) with some
                committed period of usage. Annual
                commitments renew by default.
                Commitments can be removed after their
                commitment end time passes.

                In order to remove annual commitment,
                its plan needs to be changed to monthly
                or flex first.

                A capacity commitment resource exists as
                a child resource of the admin project.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.GetCapacityCommitmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_capacity_commitment,
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

    def delete_capacity_commitment(
        self,
        request: reservation.DeleteCapacityCommitmentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a capacity commitment. Attempting to delete capacity
        commitment before its commitment_end_time will fail with the
        error code ``google.rpc.Code.FAILED_PRECONDITION``.

        Args:
            request (:class:`~.reservation.DeleteCapacityCommitmentRequest`):
                The request object. The request for
                [ReservationService.DeleteCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.DeleteCapacityCommitment].
            name (:class:`str`):
                Required. Resource name of the
                capacity commitment to delete. E.g.,
                projects/myproject/locations/US/capacityCommitments/123
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

        request = reservation.DeleteCapacityCommitmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_capacity_commitment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def update_capacity_commitment(
        self,
        request: reservation.UpdateCapacityCommitmentRequest = None,
        *,
        capacity_commitment: reservation.CapacityCommitment = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.CapacityCommitment:
        r"""Updates an existing capacity commitment.

        Only ``plan`` and ``renewal_plan`` fields can be updated.

        Plan can only be changed to a plan of a longer commitment
        period. Attempting to change to a plan with shorter commitment
        period will fail with the error code
        ``google.rpc.Code.FAILED_PRECONDITION``.

        Args:
            request (:class:`~.reservation.UpdateCapacityCommitmentRequest`):
                The request object. The request for
                [ReservationService.UpdateCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.UpdateCapacityCommitment].
            capacity_commitment (:class:`~.reservation.CapacityCommitment`):
                Content of the capacity commitment to
                update.
                This corresponds to the ``capacity_commitment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Standard field mask for the set of
                fields to be updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.reservation.CapacityCommitment:
                Capacity commitment is a way to
                purchase compute capacity for BigQuery
                jobs (in the form of slots) with some
                committed period of usage. Annual
                commitments renew by default.
                Commitments can be removed after their
                commitment end time passes.

                In order to remove annual commitment,
                its plan needs to be changed to monthly
                or flex first.

                A capacity commitment resource exists as
                a child resource of the admin project.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([capacity_commitment, update_mask]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.UpdateCapacityCommitmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if capacity_commitment is not None:
            request.capacity_commitment = capacity_commitment
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_capacity_commitment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def split_capacity_commitment(
        self,
        request: reservation.SplitCapacityCommitmentRequest = None,
        *,
        name: str = None,
        slot_count: int = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.SplitCapacityCommitmentResponse:
        r"""Splits capacity commitment to two commitments of the same plan
        and ``commitment_end_time``.

        A common use case is to enable downgrading commitments.

        For example, in order to downgrade from 10000 slots to 8000, you
        might split a 10000 capacity commitment into commitments of 2000
        and 8000. Then, you would change the plan of the first one to
        ``FLEX`` and then delete it.

        Args:
            request (:class:`~.reservation.SplitCapacityCommitmentRequest`):
                The request object. The request for
                [ReservationService.SplitCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.SplitCapacityCommitment].
            name (:class:`str`):
                Required. The resource name e.g.,:
                projects/myproject/locations/US/capacityCommitments/123
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            slot_count (:class:`int`):
                Number of slots in the capacity
                commitment after the split.
                This corresponds to the ``slot_count`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.reservation.SplitCapacityCommitmentResponse:
                The response for
                [ReservationService.SplitCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.SplitCapacityCommitment].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, slot_count]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.SplitCapacityCommitmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name
        if slot_count is not None:
            request.slot_count = slot_count

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.split_capacity_commitment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def merge_capacity_commitments(
        self,
        request: reservation.MergeCapacityCommitmentsRequest = None,
        *,
        parent: str = None,
        capacity_commitment_ids: Sequence[str] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.CapacityCommitment:
        r"""Merges capacity commitments of the same plan into a single
        commitment.

        The resulting capacity commitment has the greater
        commitment_end_time out of the to-be-merged capacity
        commitments.

        Attempting to merge capacity commitments of different plan will
        fail with the error code
        ``google.rpc.Code.FAILED_PRECONDITION``.

        Args:
            request (:class:`~.reservation.MergeCapacityCommitmentsRequest`):
                The request object. The request for
                [ReservationService.MergeCapacityCommitments][google.cloud.bigquery.reservation.v1.ReservationService.MergeCapacityCommitments].
            parent (:class:`str`):
                Parent resource that identifies admin
                project and location e.g.,
                projects/myproject/locations/us
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            capacity_commitment_ids (:class:`Sequence[str]`):
                Ids of capacity commitments to merge.
                These capacity commitments must exist
                under admin project and location
                specified in the parent.
                This corresponds to the ``capacity_commitment_ids`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.reservation.CapacityCommitment:
                Capacity commitment is a way to
                purchase compute capacity for BigQuery
                jobs (in the form of slots) with some
                committed period of usage. Annual
                commitments renew by default.
                Commitments can be removed after their
                commitment end time passes.

                In order to remove annual commitment,
                its plan needs to be changed to monthly
                or flex first.

                A capacity commitment resource exists as
                a child resource of the admin project.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, capacity_commitment_ids]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.MergeCapacityCommitmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent
        if capacity_commitment_ids is not None:
            request.capacity_commitment_ids = capacity_commitment_ids

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.merge_capacity_commitments,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def create_assignment(
        self,
        request: reservation.CreateAssignmentRequest = None,
        *,
        parent: str = None,
        assignment: reservation.Assignment = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.Assignment:
        r"""Creates an assignment object which allows the given project to
        submit jobs of a certain type using slots from the specified
        reservation.

        Currently a resource (project, folder, organization) can only
        have one assignment per each (job_type, location) combination,
        and that reservation will be used for all jobs of the matching
        type.

        Different assignments can be created on different levels of the
        projects, folders or organization hierarchy. During query
        execution, the assignment is looked up at the project, folder
        and organization levels in that order. The first assignment
        found is applied to the query.

        When creating assignments, it does not matter if other
        assignments exist at higher levels.

        Example:

        -  The organization ``organizationA`` contains two projects,
           ``project1`` and ``project2``.
        -  Assignments for all three entities (``organizationA``,
           ``project1``, and ``project2``) could all be created and
           mapped to the same or different reservations.

        Returns ``google.rpc.Code.PERMISSION_DENIED`` if user does not
        have 'bigquery.admin' permissions on the project using the
        reservation and the project that owns this reservation.

        Returns ``google.rpc.Code.INVALID_ARGUMENT`` when location of
        the assignment does not match location of the reservation.

        Args:
            request (:class:`~.reservation.CreateAssignmentRequest`):
                The request object. The request for
                [ReservationService.CreateAssignment][google.cloud.bigquery.reservation.v1.ReservationService.CreateAssignment].
                Note: "bigquery.reservationAssignments.create"
                permission is required on the related assignee.
            parent (:class:`str`):
                Required. The parent resource name of the assignment
                E.g.
                ``projects/myproject/locations/US/reservations/team1-prod``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            assignment (:class:`~.reservation.Assignment`):
                Assignment resource to create.
                This corresponds to the ``assignment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.reservation.Assignment:
                A Assignment allows a project to
                submit jobs of a certain type using
                slots from the specified reservation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, assignment]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.CreateAssignmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent
        if assignment is not None:
            request.assignment = assignment

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.create_assignment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def list_assignments(
        self,
        request: reservation.ListAssignmentsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAssignmentsPager:
        r"""Lists assignments.

        Only explicitly created assignments will be returned.

        Example:

        -  Organization ``organizationA`` contains two projects,
           ``project1`` and ``project2``.
        -  Reservation ``res1`` exists and was created previously.
        -  CreateAssignment was used previously to define the following
           associations between entities and reservations:
           ``<organizationA, res1>`` and ``<project1, res1>``

        In this example, ListAssignments will just return the above two
        assignments for reservation ``res1``, and no expansion/merge
        will happen.

        The wildcard "-" can be used for reservations in the request. In
        that case all assignments belongs to the specified project and
        location will be listed.

        **Note** "-" cannot be used for projects nor locations.

        Args:
            request (:class:`~.reservation.ListAssignmentsRequest`):
                The request object. The request for
                [ReservationService.ListAssignments][google.cloud.bigquery.reservation.v1.ReservationService.ListAssignments].
            parent (:class:`str`):
                Required. The parent resource name e.g.:

                ``projects/myproject/locations/US/reservations/team1-prod``

                Or:

                ``projects/myproject/locations/US/reservations/-``
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListAssignmentsPager:
                The response for
                [ReservationService.ListAssignments][google.cloud.bigquery.reservation.v1.ReservationService.ListAssignments].

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

        request = reservation.ListAssignmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_assignments,
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
        response = pagers.ListAssignmentsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def delete_assignment(
        self,
        request: reservation.DeleteAssignmentRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a assignment. No expansion will happen.

        Example:

        -  Organization ``organizationA`` contains two projects,
           ``project1`` and ``project2``.
        -  Reservation ``res1`` exists and was created previously.
        -  CreateAssignment was used previously to define the following
           associations between entities and reservations:
           ``<organizationA, res1>`` and ``<project1, res1>``

        In this example, deletion of the ``<organizationA, res1>``
        assignment won't affect the other assignment
        ``<project1, res1>``. After said deletion, queries from
        ``project1`` will still use ``res1`` while queries from
        ``project2`` will switch to use on-demand mode.

        Args:
            request (:class:`~.reservation.DeleteAssignmentRequest`):
                The request object. The request for
                [ReservationService.DeleteAssignment][google.cloud.bigquery.reservation.v1.ReservationService.DeleteAssignment].
                Note: "bigquery.reservationAssignments.delete"
                permission is required on the related assignee.
            name (:class:`str`):
                Required. Name of the resource, e.g.
                ``projects/myproject/locations/US/reservations/team1-prod/assignments/123``
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

        request = reservation.DeleteAssignmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_assignment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        rpc(request, retry=retry, timeout=timeout, metadata=metadata)

    def search_assignments(
        self,
        request: reservation.SearchAssignmentsRequest = None,
        *,
        parent: str = None,
        query: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchAssignmentsPager:
        r"""Looks up assignments for a specified resource for a particular
        region. If the request is about a project:

        1. Assignments created on the project will be returned if they
           exist.
        2. Otherwise assignments created on the closest ancestor will be
           returned.
        3. Assignments for different JobTypes will all be returned.

        The same logic applies if the request is about a folder.

        If the request is about an organization, then assignments
        created on the organization will be returned (organization
        doesn't have ancestors).

        Comparing to ListAssignments, there are some behavior
        differences:

        1. permission on the assignee will be verified in this API.
        2. Hierarchy lookup (project->folder->organization) happens in
           this API.
        3. Parent here is ``projects/*/locations/*``, instead of
           ``projects/*/locations/*reservations/*``.

        **Note** "-" cannot be used for projects nor locations.

        Args:
            request (:class:`~.reservation.SearchAssignmentsRequest`):
                The request object. The request for
                [ReservationService.SearchAssignments][google.cloud.bigquery.reservation.v1.ReservationService.SearchAssignments].
                Note: "bigquery.reservationAssignments.search"
                permission is required on the related assignee.
            parent (:class:`str`):
                Required. The resource name of the
                admin project(containing project and
                location), e.g.:
                "projects/myproject/locations/US".
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            query (:class:`str`):
                Please specify resource name as assignee in the query.

                Examples:

                -  ``assignee=projects/myproject``
                -  ``assignee=folders/123``
                -  ``assignee=organizations/456``

                This corresponds to the ``query`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.SearchAssignmentsPager:
                The response for
                [ReservationService.SearchAssignments][google.cloud.bigquery.reservation.v1.ReservationService.SearchAssignments].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([parent, query]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.SearchAssignmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if parent is not None:
            request.parent = parent
        if query is not None:
            request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.search_assignments,
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
        response = pagers.SearchAssignmentsPager(
            method=rpc, request=request, response=response
        )

        # Done; return the response.
        return response

    def move_assignment(
        self,
        request: reservation.MoveAssignmentRequest = None,
        *,
        name: str = None,
        destination_id: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.Assignment:
        r"""Moves an assignment under a new reservation.
        This differs from removing an existing assignment and
        recreating a new one by providing a transactional change
        that ensures an assignee always has an associated
        reservation.

        Args:
            request (:class:`~.reservation.MoveAssignmentRequest`):
                The request object. The request for
                [ReservationService.MoveAssignment][google.cloud.bigquery.reservation.v1.ReservationService.MoveAssignment].
                **Note**: "bigquery.reservationAssignments.create"
                permission is required on the destination_id.

                **Note**: "bigquery.reservationAssignments.create" and
                "bigquery.reservationAssignments.delete" permission are
                required on the related assignee.
            name (:class:`str`):
                Required. The resource name of the assignment, e.g.
                ``projects/myproject/locations/US/reservations/team1-prod/assignments/123``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            destination_id (:class:`str`):
                The new reservation ID, e.g.:
                ``projects/myotherproject/locations/US/reservations/team2-prod``
                This corresponds to the ``destination_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.reservation.Assignment:
                A Assignment allows a project to
                submit jobs of a certain type using
                slots from the specified reservation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name, destination_id]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.MoveAssignmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name
        if destination_id is not None:
            request.destination_id = destination_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.move_assignment,
            default_timeout=None,
            client_info=_client_info,
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata)

        # Done; return the response.
        return response

    def get_bi_reservation(
        self,
        request: reservation.GetBiReservationRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.BiReservation:
        r"""Retrieves a BI reservation.

        Args:
            request (:class:`~.reservation.GetBiReservationRequest`):
                The request object. A request to get a singleton BI
                reservation.
            name (:class:`str`):
                Required. Name of the requested reservation, for
                example:
                ``projects/{project_id}/locations/{location_id}/bireservation``
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.reservation.BiReservation:
                Represents a BI Reservation.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([name]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.GetBiReservationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_bi_reservation,
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

    def update_bi_reservation(
        self,
        request: reservation.UpdateBiReservationRequest = None,
        *,
        bi_reservation: reservation.BiReservation = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.BiReservation:
        r"""Updates a BI reservation.

        Only fields specified in the ``field_mask`` are updated.

        A singleton BI reservation always exists with default size 0. In
        order to reserve BI capacity it needs to be updated to an amount
        greater than 0. In order to release BI capacity reservation size
        must be set to 0.

        Args:
            request (:class:`~.reservation.UpdateBiReservationRequest`):
                The request object. A request to update a BI
                reservation.
            bi_reservation (:class:`~.reservation.BiReservation`):
                A reservation to update.
                This corresponds to the ``bi_reservation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                A list of fields to be updated in
                this request.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.reservation.BiReservation:
                Represents a BI Reservation.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([bi_reservation, update_mask]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.UpdateBiReservationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if bi_reservation is not None:
            request.bi_reservation = bi_reservation
        if update_mask is not None:
            request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.update_bi_reservation,
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
            "google-cloud-bigquery-reservation"
        ).version
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("ReservationServiceClient",)
