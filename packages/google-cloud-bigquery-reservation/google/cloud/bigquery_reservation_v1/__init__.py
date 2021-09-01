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

from .services.reservation_service import ReservationServiceClient
from .services.reservation_service import ReservationServiceAsyncClient

from .types.reservation import Assignment
from .types.reservation import BiReservation
from .types.reservation import CapacityCommitment
from .types.reservation import CreateAssignmentRequest
from .types.reservation import CreateCapacityCommitmentRequest
from .types.reservation import CreateReservationRequest
from .types.reservation import DeleteAssignmentRequest
from .types.reservation import DeleteCapacityCommitmentRequest
from .types.reservation import DeleteReservationRequest
from .types.reservation import GetBiReservationRequest
from .types.reservation import GetCapacityCommitmentRequest
from .types.reservation import GetReservationRequest
from .types.reservation import ListAssignmentsRequest
from .types.reservation import ListAssignmentsResponse
from .types.reservation import ListCapacityCommitmentsRequest
from .types.reservation import ListCapacityCommitmentsResponse
from .types.reservation import ListReservationsRequest
from .types.reservation import ListReservationsResponse
from .types.reservation import MergeCapacityCommitmentsRequest
from .types.reservation import MoveAssignmentRequest
from .types.reservation import Reservation
from .types.reservation import SearchAllAssignmentsRequest
from .types.reservation import SearchAllAssignmentsResponse
from .types.reservation import SearchAssignmentsRequest
from .types.reservation import SearchAssignmentsResponse
from .types.reservation import SplitCapacityCommitmentRequest
from .types.reservation import SplitCapacityCommitmentResponse
from .types.reservation import UpdateBiReservationRequest
from .types.reservation import UpdateCapacityCommitmentRequest
from .types.reservation import UpdateReservationRequest

__all__ = (
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
    "ReservationServiceClient",
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
