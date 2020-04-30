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

import abc
import typing

from google import auth
from google.auth import credentials  # type: ignore

from google.cloud.bigquery.reservation_v1.types import reservation
from google.cloud.bigquery.reservation_v1.types import reservation as gcbr_reservation
from google.protobuf import empty_pb2 as empty  # type: ignore


class ReservationServiceTransport(metaclass=abc.ABCMeta):
    """Abstract transport class for ReservationService."""

    AUTH_SCOPES = (
        "https://www.googleapis.com/auth/bigquery",
        "https://www.googleapis.com/auth/cloud-platform",
    )

    def __init__(
        self,
        *,
        host: str = "bigqueryreservation.googleapis.com",
        credentials: credentials.Credentials = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

    @property
    def create_reservation(
        self
    ) -> typing.Callable[
        [gcbr_reservation.CreateReservationRequest], gcbr_reservation.Reservation
    ]:
        raise NotImplementedError

    @property
    def list_reservations(
        self
    ) -> typing.Callable[
        [reservation.ListReservationsRequest], reservation.ListReservationsResponse
    ]:
        raise NotImplementedError

    @property
    def get_reservation(
        self
    ) -> typing.Callable[[reservation.GetReservationRequest], reservation.Reservation]:
        raise NotImplementedError

    @property
    def delete_reservation(
        self
    ) -> typing.Callable[[reservation.DeleteReservationRequest], empty.Empty]:
        raise NotImplementedError

    @property
    def update_reservation(
        self
    ) -> typing.Callable[
        [gcbr_reservation.UpdateReservationRequest], gcbr_reservation.Reservation
    ]:
        raise NotImplementedError

    @property
    def create_capacity_commitment(
        self
    ) -> typing.Callable[
        [reservation.CreateCapacityCommitmentRequest], reservation.CapacityCommitment
    ]:
        raise NotImplementedError

    @property
    def list_capacity_commitments(
        self
    ) -> typing.Callable[
        [reservation.ListCapacityCommitmentsRequest],
        reservation.ListCapacityCommitmentsResponse,
    ]:
        raise NotImplementedError

    @property
    def get_capacity_commitment(
        self
    ) -> typing.Callable[
        [reservation.GetCapacityCommitmentRequest], reservation.CapacityCommitment
    ]:
        raise NotImplementedError

    @property
    def delete_capacity_commitment(
        self
    ) -> typing.Callable[[reservation.DeleteCapacityCommitmentRequest], empty.Empty]:
        raise NotImplementedError

    @property
    def update_capacity_commitment(
        self
    ) -> typing.Callable[
        [reservation.UpdateCapacityCommitmentRequest], reservation.CapacityCommitment
    ]:
        raise NotImplementedError

    @property
    def split_capacity_commitment(
        self
    ) -> typing.Callable[
        [reservation.SplitCapacityCommitmentRequest],
        reservation.SplitCapacityCommitmentResponse,
    ]:
        raise NotImplementedError

    @property
    def merge_capacity_commitments(
        self
    ) -> typing.Callable[
        [reservation.MergeCapacityCommitmentsRequest], reservation.CapacityCommitment
    ]:
        raise NotImplementedError

    @property
    def create_assignment(
        self
    ) -> typing.Callable[[reservation.CreateAssignmentRequest], reservation.Assignment]:
        raise NotImplementedError

    @property
    def list_assignments(
        self
    ) -> typing.Callable[
        [reservation.ListAssignmentsRequest], reservation.ListAssignmentsResponse
    ]:
        raise NotImplementedError

    @property
    def delete_assignment(
        self
    ) -> typing.Callable[[reservation.DeleteAssignmentRequest], empty.Empty]:
        raise NotImplementedError

    @property
    def search_assignments(
        self
    ) -> typing.Callable[
        [reservation.SearchAssignmentsRequest], reservation.SearchAssignmentsResponse
    ]:
        raise NotImplementedError

    @property
    def move_assignment(
        self
    ) -> typing.Callable[[reservation.MoveAssignmentRequest], reservation.Assignment]:
        raise NotImplementedError

    @property
    def get_bi_reservation(
        self
    ) -> typing.Callable[
        [reservation.GetBiReservationRequest], reservation.BiReservation
    ]:
        raise NotImplementedError

    @property
    def update_bi_reservation(
        self
    ) -> typing.Callable[
        [reservation.UpdateBiReservationRequest], reservation.BiReservation
    ]:
        raise NotImplementedError


__all__ = ("ReservationServiceTransport",)
