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
import pkg_resources

from google import auth  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore

from google.cloud.bigquery_reservation_v1.types import reservation
from google.cloud.bigquery_reservation_v1.types import reservation as gcbr_reservation
from google.protobuf import empty_pb2 as empty  # type: ignore


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-bigquery-reservation",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


class ReservationServiceTransport(abc.ABC):
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
        credentials_file: typing.Optional[str] = None,
        scopes: typing.Optional[typing.Sequence[str]] = AUTH_SCOPES,
        quota_project_id: typing.Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scope (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):	
                The client info used to send a user-agent string along with	
                API requests. If ``None``, then default info will be used.	
                Generally, you only need to set this if you're developing	
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = auth.load_credentials_from_file(
                credentials_file, scopes=scopes, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = auth.default(
                scopes=scopes, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

        # Lifted into its own function so it can be stubbed out during tests.
        self._prep_wrapped_messages(client_info)

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_reservation: gapic_v1.method.wrap_method(
                self.create_reservation, default_timeout=60.0, client_info=client_info,
            ),
            self.list_reservations: gapic_v1.method.wrap_method(
                self.list_reservations,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_reservation: gapic_v1.method.wrap_method(
                self.get_reservation,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_reservation: gapic_v1.method.wrap_method(
                self.delete_reservation,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_reservation: gapic_v1.method.wrap_method(
                self.update_reservation, default_timeout=60.0, client_info=client_info,
            ),
            self.create_capacity_commitment: gapic_v1.method.wrap_method(
                self.create_capacity_commitment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.list_capacity_commitments: gapic_v1.method.wrap_method(
                self.list_capacity_commitments,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.get_capacity_commitment: gapic_v1.method.wrap_method(
                self.get_capacity_commitment,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_capacity_commitment: gapic_v1.method.wrap_method(
                self.delete_capacity_commitment,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_capacity_commitment: gapic_v1.method.wrap_method(
                self.update_capacity_commitment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.split_capacity_commitment: gapic_v1.method.wrap_method(
                self.split_capacity_commitment,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.merge_capacity_commitments: gapic_v1.method.wrap_method(
                self.merge_capacity_commitments,
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.create_assignment: gapic_v1.method.wrap_method(
                self.create_assignment, default_timeout=60.0, client_info=client_info,
            ),
            self.list_assignments: gapic_v1.method.wrap_method(
                self.list_assignments,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.delete_assignment: gapic_v1.method.wrap_method(
                self.delete_assignment,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.search_assignments: gapic_v1.method.wrap_method(
                self.search_assignments,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.move_assignment: gapic_v1.method.wrap_method(
                self.move_assignment, default_timeout=60.0, client_info=client_info,
            ),
            self.get_bi_reservation: gapic_v1.method.wrap_method(
                self.get_bi_reservation,
                default_retry=retries.Retry(
                    initial=0.1,
                    maximum=60.0,
                    multiplier=1.3,
                    predicate=retries.if_exception_type(
                        exceptions.DeadlineExceeded, exceptions.ServiceUnavailable,
                    ),
                ),
                default_timeout=60.0,
                client_info=client_info,
            ),
            self.update_bi_reservation: gapic_v1.method.wrap_method(
                self.update_bi_reservation,
                default_timeout=60.0,
                client_info=client_info,
            ),
        }

    @property
    def create_reservation(
        self,
    ) -> typing.Callable[
        [gcbr_reservation.CreateReservationRequest],
        typing.Union[
            gcbr_reservation.Reservation, typing.Awaitable[gcbr_reservation.Reservation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_reservations(
        self,
    ) -> typing.Callable[
        [reservation.ListReservationsRequest],
        typing.Union[
            reservation.ListReservationsResponse,
            typing.Awaitable[reservation.ListReservationsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_reservation(
        self,
    ) -> typing.Callable[
        [reservation.GetReservationRequest],
        typing.Union[
            reservation.Reservation, typing.Awaitable[reservation.Reservation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_reservation(
        self,
    ) -> typing.Callable[
        [reservation.DeleteReservationRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_reservation(
        self,
    ) -> typing.Callable[
        [gcbr_reservation.UpdateReservationRequest],
        typing.Union[
            gcbr_reservation.Reservation, typing.Awaitable[gcbr_reservation.Reservation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_capacity_commitment(
        self,
    ) -> typing.Callable[
        [reservation.CreateCapacityCommitmentRequest],
        typing.Union[
            reservation.CapacityCommitment,
            typing.Awaitable[reservation.CapacityCommitment],
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_capacity_commitments(
        self,
    ) -> typing.Callable[
        [reservation.ListCapacityCommitmentsRequest],
        typing.Union[
            reservation.ListCapacityCommitmentsResponse,
            typing.Awaitable[reservation.ListCapacityCommitmentsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_capacity_commitment(
        self,
    ) -> typing.Callable[
        [reservation.GetCapacityCommitmentRequest],
        typing.Union[
            reservation.CapacityCommitment,
            typing.Awaitable[reservation.CapacityCommitment],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_capacity_commitment(
        self,
    ) -> typing.Callable[
        [reservation.DeleteCapacityCommitmentRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def update_capacity_commitment(
        self,
    ) -> typing.Callable[
        [reservation.UpdateCapacityCommitmentRequest],
        typing.Union[
            reservation.CapacityCommitment,
            typing.Awaitable[reservation.CapacityCommitment],
        ],
    ]:
        raise NotImplementedError()

    @property
    def split_capacity_commitment(
        self,
    ) -> typing.Callable[
        [reservation.SplitCapacityCommitmentRequest],
        typing.Union[
            reservation.SplitCapacityCommitmentResponse,
            typing.Awaitable[reservation.SplitCapacityCommitmentResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def merge_capacity_commitments(
        self,
    ) -> typing.Callable[
        [reservation.MergeCapacityCommitmentsRequest],
        typing.Union[
            reservation.CapacityCommitment,
            typing.Awaitable[reservation.CapacityCommitment],
        ],
    ]:
        raise NotImplementedError()

    @property
    def create_assignment(
        self,
    ) -> typing.Callable[
        [reservation.CreateAssignmentRequest],
        typing.Union[reservation.Assignment, typing.Awaitable[reservation.Assignment]],
    ]:
        raise NotImplementedError()

    @property
    def list_assignments(
        self,
    ) -> typing.Callable[
        [reservation.ListAssignmentsRequest],
        typing.Union[
            reservation.ListAssignmentsResponse,
            typing.Awaitable[reservation.ListAssignmentsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_assignment(
        self,
    ) -> typing.Callable[
        [reservation.DeleteAssignmentRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def search_assignments(
        self,
    ) -> typing.Callable[
        [reservation.SearchAssignmentsRequest],
        typing.Union[
            reservation.SearchAssignmentsResponse,
            typing.Awaitable[reservation.SearchAssignmentsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def move_assignment(
        self,
    ) -> typing.Callable[
        [reservation.MoveAssignmentRequest],
        typing.Union[reservation.Assignment, typing.Awaitable[reservation.Assignment]],
    ]:
        raise NotImplementedError()

    @property
    def get_bi_reservation(
        self,
    ) -> typing.Callable[
        [reservation.GetBiReservationRequest],
        typing.Union[
            reservation.BiReservation, typing.Awaitable[reservation.BiReservation]
        ],
    ]:
        raise NotImplementedError()

    @property
    def update_bi_reservation(
        self,
    ) -> typing.Callable[
        [reservation.UpdateBiReservationRequest],
        typing.Union[
            reservation.BiReservation, typing.Awaitable[reservation.BiReservation]
        ],
    ]:
        raise NotImplementedError()


__all__ = ("ReservationServiceTransport",)
