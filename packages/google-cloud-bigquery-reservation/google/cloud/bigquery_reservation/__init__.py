# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from google.cloud.bigquery_reservation import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.bigquery_reservation_v1.services.reservation_service.async_client import (
    ReservationServiceAsyncClient,
)
from google.cloud.bigquery_reservation_v1.services.reservation_service.client import (
    ReservationServiceClient,
)
from google.cloud.bigquery_reservation_v1.types.reservation import (
    Assignment,
    BiReservation,
    CapacityCommitment,
    CreateAssignmentRequest,
    CreateCapacityCommitmentRequest,
    CreateReservationRequest,
    DeleteAssignmentRequest,
    DeleteCapacityCommitmentRequest,
    DeleteReservationRequest,
    Edition,
    FailoverReservationRequest,
    GetBiReservationRequest,
    GetCapacityCommitmentRequest,
    GetReservationRequest,
    ListAssignmentsRequest,
    ListAssignmentsResponse,
    ListCapacityCommitmentsRequest,
    ListCapacityCommitmentsResponse,
    ListReservationsRequest,
    ListReservationsResponse,
    MergeCapacityCommitmentsRequest,
    MoveAssignmentRequest,
    Reservation,
    SearchAllAssignmentsRequest,
    SearchAllAssignmentsResponse,
    SearchAssignmentsRequest,
    SearchAssignmentsResponse,
    SplitCapacityCommitmentRequest,
    SplitCapacityCommitmentResponse,
    TableReference,
    UpdateAssignmentRequest,
    UpdateBiReservationRequest,
    UpdateCapacityCommitmentRequest,
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
    "FailoverReservationRequest",
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
    "TableReference",
    "UpdateAssignmentRequest",
    "UpdateBiReservationRequest",
    "UpdateCapacityCommitmentRequest",
    "UpdateReservationRequest",
    "Edition",
)
