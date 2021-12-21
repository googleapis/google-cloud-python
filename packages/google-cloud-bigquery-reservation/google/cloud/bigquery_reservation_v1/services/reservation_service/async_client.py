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

from google.cloud.bigquery_reservation_v1.services.reservation_service import pagers
from google.cloud.bigquery_reservation_v1.types import reservation
from google.cloud.bigquery_reservation_v1.types import reservation as gcbr_reservation
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from .transports.base import ReservationServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ReservationServiceGrpcAsyncIOTransport
from .client import ReservationServiceClient


class ReservationServiceAsyncClient:
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

    _client: ReservationServiceClient

    DEFAULT_ENDPOINT = ReservationServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ReservationServiceClient.DEFAULT_MTLS_ENDPOINT

    assignment_path = staticmethod(ReservationServiceClient.assignment_path)
    parse_assignment_path = staticmethod(ReservationServiceClient.parse_assignment_path)
    bi_reservation_path = staticmethod(ReservationServiceClient.bi_reservation_path)
    parse_bi_reservation_path = staticmethod(
        ReservationServiceClient.parse_bi_reservation_path
    )
    capacity_commitment_path = staticmethod(
        ReservationServiceClient.capacity_commitment_path
    )
    parse_capacity_commitment_path = staticmethod(
        ReservationServiceClient.parse_capacity_commitment_path
    )
    reservation_path = staticmethod(ReservationServiceClient.reservation_path)
    parse_reservation_path = staticmethod(
        ReservationServiceClient.parse_reservation_path
    )
    common_billing_account_path = staticmethod(
        ReservationServiceClient.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        ReservationServiceClient.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(ReservationServiceClient.common_folder_path)
    parse_common_folder_path = staticmethod(
        ReservationServiceClient.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        ReservationServiceClient.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        ReservationServiceClient.parse_common_organization_path
    )
    common_project_path = staticmethod(ReservationServiceClient.common_project_path)
    parse_common_project_path = staticmethod(
        ReservationServiceClient.parse_common_project_path
    )
    common_location_path = staticmethod(ReservationServiceClient.common_location_path)
    parse_common_location_path = staticmethod(
        ReservationServiceClient.parse_common_location_path
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
            ReservationServiceAsyncClient: The constructed client.
        """
        return ReservationServiceClient.from_service_account_info.__func__(ReservationServiceAsyncClient, info, *args, **kwargs)  # type: ignore

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
            ReservationServiceAsyncClient: The constructed client.
        """
        return ReservationServiceClient.from_service_account_file.__func__(ReservationServiceAsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> ReservationServiceTransport:
        """Returns the transport used by the client instance.

        Returns:
            ReservationServiceTransport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(ReservationServiceClient).get_transport_class,
        type(ReservationServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, ReservationServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the reservation service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ReservationServiceTransport]): The
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
        self._client = ReservationServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def create_reservation(
        self,
        request: Union[gcbr_reservation.CreateReservationRequest, dict] = None,
        *,
        parent: str = None,
        reservation: gcbr_reservation.Reservation = None,
        reservation_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcbr_reservation.Reservation:
        r"""Creates a new reservation resource.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.CreateReservationRequest, dict]):
                The request object. The request for
                [ReservationService.CreateReservation][google.cloud.bigquery.reservation.v1.ReservationService.CreateReservation].
            parent (:class:`str`):
                Required. Project, location. E.g.,
                ``projects/myproject/locations/US``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            reservation (:class:`google.cloud.bigquery_reservation_v1.types.Reservation`):
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
            google.cloud.bigquery_reservation_v1.types.Reservation:
                A reservation is a mechanism used to
                guarantee slots to users.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, reservation, reservation_id])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_reservation,
            default_timeout=300.0,
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

    async def list_reservations(
        self,
        request: Union[reservation.ListReservationsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListReservationsAsyncPager:
        r"""Lists all the reservations for the project in the
        specified location.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.ListReservationsRequest, dict]):
                The request object. The request for
                [ReservationService.ListReservations][google.cloud.bigquery.reservation.v1.ReservationService.ListReservations].
            parent (:class:`str`):
                Required. The parent resource name containing project
                and location, e.g.: ``projects/myproject/locations/US``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_reservation_v1.services.reservation_service.pagers.ListReservationsAsyncPager:
                The response for
                [ReservationService.ListReservations][google.cloud.bigquery.reservation.v1.ReservationService.ListReservations].

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

        request = reservation.ListReservationsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_reservations,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
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
        response = pagers.ListReservationsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_reservation(
        self,
        request: Union[reservation.GetReservationRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.Reservation:
        r"""Returns information about the reservation.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.GetReservationRequest, dict]):
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
            google.cloud.bigquery_reservation_v1.types.Reservation:
                A reservation is a mechanism used to
                guarantee slots to users.

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

        request = reservation.GetReservationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_reservation,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
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

    async def delete_reservation(
        self,
        request: Union[reservation.DeleteReservationRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a reservation. Returns
        ``google.rpc.Code.FAILED_PRECONDITION`` when reservation has
        assignments.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.DeleteReservationRequest, dict]):
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
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_reservation,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
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

    async def update_reservation(
        self,
        request: Union[gcbr_reservation.UpdateReservationRequest, dict] = None,
        *,
        reservation: gcbr_reservation.Reservation = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gcbr_reservation.Reservation:
        r"""Updates an existing reservation resource.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.UpdateReservationRequest, dict]):
                The request object. The request for
                [ReservationService.UpdateReservation][google.cloud.bigquery.reservation.v1.ReservationService.UpdateReservation].
            reservation (:class:`google.cloud.bigquery_reservation_v1.types.Reservation`):
                Content of the reservation to update.
                This corresponds to the ``reservation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
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
            google.cloud.bigquery_reservation_v1.types.Reservation:
                A reservation is a mechanism used to
                guarantee slots to users.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([reservation, update_mask])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_reservation,
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("reservation.name", request.reservation.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def create_capacity_commitment(
        self,
        request: Union[reservation.CreateCapacityCommitmentRequest, dict] = None,
        *,
        parent: str = None,
        capacity_commitment: reservation.CapacityCommitment = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.CapacityCommitment:
        r"""Creates a new capacity commitment resource.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.CreateCapacityCommitmentRequest, dict]):
                The request object. The request for
                [ReservationService.CreateCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.CreateCapacityCommitment].
            parent (:class:`str`):
                Required. Resource name of the parent reservation. E.g.,
                ``projects/myproject/locations/US``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            capacity_commitment (:class:`google.cloud.bigquery_reservation_v1.types.CapacityCommitment`):
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
            google.cloud.bigquery_reservation_v1.types.CapacityCommitment:
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
        has_flattened_params = any([parent, capacity_commitment])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_capacity_commitment,
            default_timeout=300.0,
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

    async def list_capacity_commitments(
        self,
        request: Union[reservation.ListCapacityCommitmentsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListCapacityCommitmentsAsyncPager:
        r"""Lists all the capacity commitments for the admin
        project.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.ListCapacityCommitmentsRequest, dict]):
                The request object. The request for
                [ReservationService.ListCapacityCommitments][google.cloud.bigquery.reservation.v1.ReservationService.ListCapacityCommitments].
            parent (:class:`str`):
                Required. Resource name of the parent reservation. E.g.,
                ``projects/myproject/locations/US``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_reservation_v1.services.reservation_service.pagers.ListCapacityCommitmentsAsyncPager:
                The response for
                [ReservationService.ListCapacityCommitments][google.cloud.bigquery.reservation.v1.ReservationService.ListCapacityCommitments].

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

        request = reservation.ListCapacityCommitmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_capacity_commitments,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
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
        response = pagers.ListCapacityCommitmentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def get_capacity_commitment(
        self,
        request: Union[reservation.GetCapacityCommitmentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.CapacityCommitment:
        r"""Returns information about the capacity commitment.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.GetCapacityCommitmentRequest, dict]):
                The request object. The request for
                [ReservationService.GetCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.GetCapacityCommitment].
            name (:class:`str`):
                Required. Resource name of the capacity commitment to
                retrieve. E.g.,
                ``projects/myproject/locations/US/capacityCommitments/123``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_reservation_v1.types.CapacityCommitment:
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
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_capacity_commitment,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
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

    async def delete_capacity_commitment(
        self,
        request: Union[reservation.DeleteCapacityCommitmentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a capacity commitment. Attempting to delete capacity
        commitment before its commitment_end_time will fail with the
        error code ``google.rpc.Code.FAILED_PRECONDITION``.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.DeleteCapacityCommitmentRequest, dict]):
                The request object. The request for
                [ReservationService.DeleteCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.DeleteCapacityCommitment].
            name (:class:`str`):
                Required. Resource name of the capacity commitment to
                delete. E.g.,
                ``projects/myproject/locations/US/capacityCommitments/123``

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

        request = reservation.DeleteCapacityCommitmentRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_capacity_commitment,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
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

    async def update_capacity_commitment(
        self,
        request: Union[reservation.UpdateCapacityCommitmentRequest, dict] = None,
        *,
        capacity_commitment: reservation.CapacityCommitment = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
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
            request (Union[google.cloud.bigquery_reservation_v1.types.UpdateCapacityCommitmentRequest, dict]):
                The request object. The request for
                [ReservationService.UpdateCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.UpdateCapacityCommitment].
            capacity_commitment (:class:`google.cloud.bigquery_reservation_v1.types.CapacityCommitment`):
                Content of the capacity commitment to
                update.

                This corresponds to the ``capacity_commitment`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
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
            google.cloud.bigquery_reservation_v1.types.CapacityCommitment:
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
        has_flattened_params = any([capacity_commitment, update_mask])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_capacity_commitment,
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("capacity_commitment.name", request.capacity_commitment.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def split_capacity_commitment(
        self,
        request: Union[reservation.SplitCapacityCommitmentRequest, dict] = None,
        *,
        name: str = None,
        slot_count: int = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
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
            request (Union[google.cloud.bigquery_reservation_v1.types.SplitCapacityCommitmentRequest, dict]):
                The request object. The request for
                [ReservationService.SplitCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.SplitCapacityCommitment].
            name (:class:`str`):
                Required. The resource name e.g.,:
                ``projects/myproject/locations/US/capacityCommitments/123``

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
            google.cloud.bigquery_reservation_v1.types.SplitCapacityCommitmentResponse:
                The response for
                [ReservationService.SplitCapacityCommitment][google.cloud.bigquery.reservation.v1.ReservationService.SplitCapacityCommitment].

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, slot_count])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.split_capacity_commitment,
            default_timeout=300.0,
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

    async def merge_capacity_commitments(
        self,
        request: Union[reservation.MergeCapacityCommitmentsRequest, dict] = None,
        *,
        parent: str = None,
        capacity_commitment_ids: Sequence[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
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
            request (Union[google.cloud.bigquery_reservation_v1.types.MergeCapacityCommitmentsRequest, dict]):
                The request object. The request for
                [ReservationService.MergeCapacityCommitments][google.cloud.bigquery.reservation.v1.ReservationService.MergeCapacityCommitments].
            parent (:class:`str`):
                Parent resource that identifies admin project and
                location e.g., ``projects/myproject/locations/us``

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            capacity_commitment_ids (:class:`Sequence[str]`):
                Ids of capacity commitments to merge.
                These capacity commitments must exist
                under admin project and location
                specified in the parent.
                ID is the last portion of capacity
                commitment name e.g., 'abc' for
                projects/myproject/locations/US/capacityCommitments/abc

                This corresponds to the ``capacity_commitment_ids`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_reservation_v1.types.CapacityCommitment:
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
        has_flattened_params = any([parent, capacity_commitment_ids])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.MergeCapacityCommitmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if capacity_commitment_ids:
            request.capacity_commitment_ids.extend(capacity_commitment_ids)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.merge_capacity_commitments,
            default_timeout=300.0,
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

    async def create_assignment(
        self,
        request: Union[reservation.CreateAssignmentRequest, dict] = None,
        *,
        parent: str = None,
        assignment: reservation.Assignment = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
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

        "None" assignments represent an absence of the assignment.
        Projects assigned to None use on-demand pricing. To create a
        "None" assignment, use "none" as a reservation_id in the parent.
        Example parent:
        ``projects/myproject/locations/US/reservations/none``.

        Returns ``google.rpc.Code.PERMISSION_DENIED`` if user does not
        have 'bigquery.admin' permissions on the project using the
        reservation and the project that owns this reservation.

        Returns ``google.rpc.Code.INVALID_ARGUMENT`` when location of
        the assignment does not match location of the reservation.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.CreateAssignmentRequest, dict]):
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
            assignment (:class:`google.cloud.bigquery_reservation_v1.types.Assignment`):
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
            google.cloud.bigquery_reservation_v1.types.Assignment:
                A Assignment allows a project to
                submit jobs of a certain type using
                slots from the specified reservation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, assignment])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.create_assignment,
            default_timeout=300.0,
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

    async def list_assignments(
        self,
        request: Union[reservation.ListAssignmentsRequest, dict] = None,
        *,
        parent: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListAssignmentsAsyncPager:
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
            request (Union[google.cloud.bigquery_reservation_v1.types.ListAssignmentsRequest, dict]):
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
            google.cloud.bigquery_reservation_v1.services.reservation_service.pagers.ListAssignmentsAsyncPager:
                The response for
                [ReservationService.ListAssignments][google.cloud.bigquery.reservation.v1.ReservationService.ListAssignments].

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

        request = reservation.ListAssignmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_assignments,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
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
        response = pagers.ListAssignmentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def delete_assignment(
        self,
        request: Union[reservation.DeleteAssignmentRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
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
            request (Union[google.cloud.bigquery_reservation_v1.types.DeleteAssignmentRequest, dict]):
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
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_assignment,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
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

    async def search_assignments(
        self,
        request: Union[reservation.SearchAssignmentsRequest, dict] = None,
        *,
        parent: str = None,
        query: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchAssignmentsAsyncPager:
        r"""Deprecated: Looks up assignments for a specified resource for a
        particular region. If the request is about a project:

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
            request (Union[google.cloud.bigquery_reservation_v1.types.SearchAssignmentsRequest, dict]):
                The request object. The request for
                [ReservationService.SearchAssignments][google.cloud.bigquery.reservation.v1.ReservationService.SearchAssignments].
                Note: "bigquery.reservationAssignments.search"
                permission is required on the related assignee.
            parent (:class:`str`):
                Required. The resource name of the admin
                project(containing project and location), e.g.:
                ``projects/myproject/locations/US``.

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
            google.cloud.bigquery_reservation_v1.services.reservation_service.pagers.SearchAssignmentsAsyncPager:
                The response for
                [ReservationService.SearchAssignments][google.cloud.bigquery.reservation.v1.ReservationService.SearchAssignments].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        warnings.warn(
            "ReservationServiceAsyncClient.search_assignments is deprecated",
            DeprecationWarning,
        )

        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, query])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_assignments,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
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
        response = pagers.SearchAssignmentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def search_all_assignments(
        self,
        request: Union[reservation.SearchAllAssignmentsRequest, dict] = None,
        *,
        parent: str = None,
        query: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.SearchAllAssignmentsAsyncPager:
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

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.SearchAllAssignmentsRequest, dict]):
                The request object. The request for
                [ReservationService.SearchAllAssignments][google.cloud.bigquery.reservation.v1.ReservationService.SearchAllAssignments].
                Note: "bigquery.reservationAssignments.search"
                permission is required on the related assignee.
            parent (:class:`str`):
                Required. The resource name with location (project name
                could be the wildcard '-'), e.g.:
                ``projects/-/locations/US``.

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
            google.cloud.bigquery_reservation_v1.services.reservation_service.pagers.SearchAllAssignmentsAsyncPager:
                The response for
                [ReservationService.SearchAllAssignments][google.cloud.bigquery.reservation.v1.ReservationService.SearchAllAssignments].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, query])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = reservation.SearchAllAssignmentsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent
        if query is not None:
            request.query = query

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.search_all_assignments,
            default_timeout=None,
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
        response = pagers.SearchAllAssignmentsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def move_assignment(
        self,
        request: Union[reservation.MoveAssignmentRequest, dict] = None,
        *,
        name: str = None,
        destination_id: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.Assignment:
        r"""Moves an assignment under a new reservation.
        This differs from removing an existing assignment and
        recreating a new one by providing a transactional change
        that ensures an assignee always has an associated
        reservation.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.MoveAssignmentRequest, dict]):
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
            google.cloud.bigquery_reservation_v1.types.Assignment:
                A Assignment allows a project to
                submit jobs of a certain type using
                slots from the specified reservation.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, destination_id])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.move_assignment,
            default_timeout=300.0,
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

    async def get_bi_reservation(
        self,
        request: Union[reservation.GetBiReservationRequest, dict] = None,
        *,
        name: str = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> reservation.BiReservation:
        r"""Retrieves a BI reservation.

        Args:
            request (Union[google.cloud.bigquery_reservation_v1.types.GetBiReservationRequest, dict]):
                The request object. A request to get a singleton BI
                reservation.
            name (:class:`str`):
                Required. Name of the requested reservation, for
                example:
                ``projects/{project_id}/locations/{location_id}/biReservation``

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.bigquery_reservation_v1.types.BiReservation:
                Represents a BI Reservation.
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

        request = reservation.GetBiReservationRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if name is not None:
            request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.get_bi_reservation,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=300.0,
            ),
            default_timeout=300.0,
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

    async def update_bi_reservation(
        self,
        request: Union[reservation.UpdateBiReservationRequest, dict] = None,
        *,
        bi_reservation: reservation.BiReservation = None,
        update_mask: field_mask_pb2.FieldMask = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
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
            request (Union[google.cloud.bigquery_reservation_v1.types.UpdateBiReservationRequest, dict]):
                The request object. A request to update a BI
                reservation.
            bi_reservation (:class:`google.cloud.bigquery_reservation_v1.types.BiReservation`):
                A reservation to update.
                This corresponds to the ``bi_reservation`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`google.protobuf.field_mask_pb2.FieldMask`):
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
            google.cloud.bigquery_reservation_v1.types.BiReservation:
                Represents a BI Reservation.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([bi_reservation, update_mask])
        if request is not None and has_flattened_params:
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
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.update_bi_reservation,
            default_timeout=300.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("bi_reservation.name", request.bi_reservation.name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.transport.close()


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigquery-reservation",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ReservationServiceAsyncClient",)
