# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.bigquery_reservation_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.reservation_service import ReservationServiceClient
from .services.reservation_service import ReservationServiceAsyncClient

from .types.reservation import Assignment
from .types.reservation import BiReservation
from .types.reservation import CapacityCommitment
from .types.reservation import CreateAssignmentRequest
from .types.reservation import CreateCapacityCommitmentRequest
from .types.reservation import CreateReservationGroupRequest
from .types.reservation import CreateReservationRequest
from .types.reservation import DeleteAssignmentRequest
from .types.reservation import DeleteCapacityCommitmentRequest
from .types.reservation import DeleteReservationGroupRequest
from .types.reservation import DeleteReservationRequest
from .types.reservation import FailoverReservationRequest
from .types.reservation import GetBiReservationRequest
from .types.reservation import GetCapacityCommitmentRequest
from .types.reservation import GetReservationGroupRequest
from .types.reservation import GetReservationRequest
from .types.reservation import ListAssignmentsRequest
from .types.reservation import ListAssignmentsResponse
from .types.reservation import ListCapacityCommitmentsRequest
from .types.reservation import ListCapacityCommitmentsResponse
from .types.reservation import ListReservationGroupsRequest
from .types.reservation import ListReservationGroupsResponse
from .types.reservation import ListReservationsRequest
from .types.reservation import ListReservationsResponse
from .types.reservation import MergeCapacityCommitmentsRequest
from .types.reservation import MoveAssignmentRequest
from .types.reservation import Reservation
from .types.reservation import ReservationGroup
from .types.reservation import SchedulingPolicy
from .types.reservation import SearchAllAssignmentsRequest
from .types.reservation import SearchAllAssignmentsResponse
from .types.reservation import SearchAssignmentsRequest
from .types.reservation import SearchAssignmentsResponse
from .types.reservation import SplitCapacityCommitmentRequest
from .types.reservation import SplitCapacityCommitmentResponse
from .types.reservation import TableReference
from .types.reservation import UpdateAssignmentRequest
from .types.reservation import UpdateBiReservationRequest
from .types.reservation import UpdateCapacityCommitmentRequest
from .types.reservation import UpdateReservationRequest
from .types.reservation import Edition
from .types.reservation import FailoverMode

__all__ = (
    'ReservationServiceAsyncClient',
'Assignment',
'BiReservation',
'CapacityCommitment',
'CreateAssignmentRequest',
'CreateCapacityCommitmentRequest',
'CreateReservationGroupRequest',
'CreateReservationRequest',
'DeleteAssignmentRequest',
'DeleteCapacityCommitmentRequest',
'DeleteReservationGroupRequest',
'DeleteReservationRequest',
'Edition',
'FailoverMode',
'FailoverReservationRequest',
'GetBiReservationRequest',
'GetCapacityCommitmentRequest',
'GetReservationGroupRequest',
'GetReservationRequest',
'ListAssignmentsRequest',
'ListAssignmentsResponse',
'ListCapacityCommitmentsRequest',
'ListCapacityCommitmentsResponse',
'ListReservationGroupsRequest',
'ListReservationGroupsResponse',
'ListReservationsRequest',
'ListReservationsResponse',
'MergeCapacityCommitmentsRequest',
'MoveAssignmentRequest',
'Reservation',
'ReservationGroup',
'ReservationServiceClient',
'SchedulingPolicy',
'SearchAllAssignmentsRequest',
'SearchAllAssignmentsResponse',
'SearchAssignmentsRequest',
'SearchAssignmentsResponse',
'SplitCapacityCommitmentRequest',
'SplitCapacityCommitmentResponse',
'TableReference',
'UpdateAssignmentRequest',
'UpdateBiReservationRequest',
'UpdateCapacityCommitmentRequest',
'UpdateReservationRequest',
)
