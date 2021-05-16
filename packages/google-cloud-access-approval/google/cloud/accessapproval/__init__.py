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

from google.cloud.accessapproval_v1.services.access_approval.client import (
    AccessApprovalClient,
)
from google.cloud.accessapproval_v1.services.access_approval.async_client import (
    AccessApprovalAsyncClient,
)

from google.cloud.accessapproval_v1.types.accessapproval import AccessApprovalSettings
from google.cloud.accessapproval_v1.types.accessapproval import AccessLocations
from google.cloud.accessapproval_v1.types.accessapproval import AccessReason
from google.cloud.accessapproval_v1.types.accessapproval import ApprovalRequest
from google.cloud.accessapproval_v1.types.accessapproval import (
    ApproveApprovalRequestMessage,
)
from google.cloud.accessapproval_v1.types.accessapproval import ApproveDecision
from google.cloud.accessapproval_v1.types.accessapproval import (
    DeleteAccessApprovalSettingsMessage,
)
from google.cloud.accessapproval_v1.types.accessapproval import (
    DismissApprovalRequestMessage,
)
from google.cloud.accessapproval_v1.types.accessapproval import DismissDecision
from google.cloud.accessapproval_v1.types.accessapproval import EnrolledService
from google.cloud.accessapproval_v1.types.accessapproval import (
    GetAccessApprovalSettingsMessage,
)
from google.cloud.accessapproval_v1.types.accessapproval import (
    GetApprovalRequestMessage,
)
from google.cloud.accessapproval_v1.types.accessapproval import (
    ListApprovalRequestsMessage,
)
from google.cloud.accessapproval_v1.types.accessapproval import (
    ListApprovalRequestsResponse,
)
from google.cloud.accessapproval_v1.types.accessapproval import ResourceProperties
from google.cloud.accessapproval_v1.types.accessapproval import (
    UpdateAccessApprovalSettingsMessage,
)
from google.cloud.accessapproval_v1.types.accessapproval import EnrollmentLevel

__all__ = (
    "AccessApprovalClient",
    "AccessApprovalAsyncClient",
    "AccessApprovalSettings",
    "AccessLocations",
    "AccessReason",
    "ApprovalRequest",
    "ApproveApprovalRequestMessage",
    "ApproveDecision",
    "DeleteAccessApprovalSettingsMessage",
    "DismissApprovalRequestMessage",
    "DismissDecision",
    "EnrolledService",
    "GetAccessApprovalSettingsMessage",
    "GetApprovalRequestMessage",
    "ListApprovalRequestsMessage",
    "ListApprovalRequestsResponse",
    "ResourceProperties",
    "UpdateAccessApprovalSettingsMessage",
    "EnrollmentLevel",
)
