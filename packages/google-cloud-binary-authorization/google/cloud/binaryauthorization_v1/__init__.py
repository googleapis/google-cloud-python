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

from .services.binauthz_management_service_v1 import BinauthzManagementServiceV1Client
from .services.binauthz_management_service_v1 import (
    BinauthzManagementServiceV1AsyncClient,
)
from .services.system_policy_v1 import SystemPolicyV1Client
from .services.system_policy_v1 import SystemPolicyV1AsyncClient
from .services.validation_helper_v1 import ValidationHelperV1Client
from .services.validation_helper_v1 import ValidationHelperV1AsyncClient

from .types.resources import AdmissionRule
from .types.resources import AdmissionWhitelistPattern
from .types.resources import Attestor
from .types.resources import AttestorPublicKey
from .types.resources import PkixPublicKey
from .types.resources import Policy
from .types.resources import UserOwnedGrafeasNote
from .types.service import CreateAttestorRequest
from .types.service import DeleteAttestorRequest
from .types.service import GetAttestorRequest
from .types.service import GetPolicyRequest
from .types.service import GetSystemPolicyRequest
from .types.service import ListAttestorsRequest
from .types.service import ListAttestorsResponse
from .types.service import UpdateAttestorRequest
from .types.service import UpdatePolicyRequest
from .types.service import ValidateAttestationOccurrenceRequest
from .types.service import ValidateAttestationOccurrenceResponse

__all__ = (
    "BinauthzManagementServiceV1AsyncClient",
    "SystemPolicyV1AsyncClient",
    "ValidationHelperV1AsyncClient",
    "AdmissionRule",
    "AdmissionWhitelistPattern",
    "Attestor",
    "AttestorPublicKey",
    "BinauthzManagementServiceV1Client",
    "CreateAttestorRequest",
    "DeleteAttestorRequest",
    "GetAttestorRequest",
    "GetPolicyRequest",
    "GetSystemPolicyRequest",
    "ListAttestorsRequest",
    "ListAttestorsResponse",
    "PkixPublicKey",
    "Policy",
    "SystemPolicyV1Client",
    "UpdateAttestorRequest",
    "UpdatePolicyRequest",
    "UserOwnedGrafeasNote",
    "ValidateAttestationOccurrenceRequest",
    "ValidateAttestationOccurrenceResponse",
    "ValidationHelperV1Client",
)
