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

from google.cloud.bigquery_reservation_v1.services.reservation_service.client import (
    ReservationServiceClient,
)
from google.cloud.bigquery_reservation_v1.services.reservation_service.async_client import (
    ReservationServiceAsyncClient,
)

from google.cloud.bigquery_reservation_v1.types.reservation import Assignment
from google.cloud.bigquery_reservation_v1.types.reservation import BiReservation
from google.cloud.bigquery_reservation_v1.types.reservation import CapacityCommitment
from google.cloud.bigquery_reservation_v1.types.reservation import (
    CreateAssignmentRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    CreateCapacityCommitmentRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    CreateReservationRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    DeleteAssignmentRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    DeleteCapacityCommitmentRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    DeleteReservationRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    GetBiReservationRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    GetCapacityCommitmentRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import GetReservationRequest
from google.cloud.bigquery_reservation_v1.types.reservation import (
    ListAssignmentsRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    ListAssignmentsResponse,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    ListCapacityCommitmentsRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    ListCapacityCommitmentsResponse,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    ListReservationsRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    ListReservationsResponse,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    MergeCapacityCommitmentsRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import MoveAssignmentRequest
from google.cloud.bigquery_reservation_v1.types.reservation import Reservation
from google.cloud.bigquery_reservation_v1.types.reservation import (
    SearchAllAssignmentsRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    SearchAllAssignmentsResponse,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    SearchAssignmentsRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    SearchAssignmentsResponse,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    SplitCapacityCommitmentRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    SplitCapacityCommitmentResponse,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    UpdateBiReservationRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    UpdateCapacityCommitmentRequest,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    UpdateReservationRequest,
)

__all__ = (
    "ReservationServiceClient",
    "ReservationServiceAsyncClient",
    "Assignment",
    "BiReservation",
    "CapacityCommitment",
    "CreateAssignmentRequest",
    "CreateCapacityCommitmentRequest",
    "CreateReservationRequest",
    "DeleteAssignmentRequest",
    "DeleteCapacityCommitmentRequest",
    "DeleteReservationRequest",
    "GetBiReservationRequest",
    "GetCapacityCommitmentRequest",
    "GetReservationRequest",
    "ListAssignmentsRequest",
    "ListAssignmentsResponse",
    "ListCapacityCommitmentsRequest",
    "ListCapacityCommitmentsResponse",
    "ListReservationsRequest",
    "ListReservationsResponse",
    "MergeCapacityCommitmentsRequest",
    "MoveAssignmentRequest",
    "Reservation",
    "SearchAllAssignmentsRequest",
    "SearchAllAssignmentsResponse",
    "SearchAssignmentsRequest",
    "SearchAssignmentsResponse",
    "SplitCapacityCommitmentRequest",
    "SplitCapacityCommitmentResponse",
    "UpdateBiReservationRequest",
    "UpdateCapacityCommitmentRequest",
    "UpdateReservationRequest",
)
