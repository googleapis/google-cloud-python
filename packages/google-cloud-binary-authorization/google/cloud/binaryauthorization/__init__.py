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

from google.cloud.binaryauthorization_v1beta1.services.binauthz_management_service_v1_beta1.async_client import (
    BinauthzManagementServiceV1Beta1AsyncClient,
)
from google.cloud.binaryauthorization_v1beta1.services.binauthz_management_service_v1_beta1.client import (
    BinauthzManagementServiceV1Beta1Client,
)
from google.cloud.binaryauthorization_v1beta1.types.resources import AdmissionRule
from google.cloud.binaryauthorization_v1beta1.types.resources import (
    AdmissionWhitelistPattern,
)
from google.cloud.binaryauthorization_v1beta1.types.resources import Attestor
from google.cloud.binaryauthorization_v1beta1.types.resources import AttestorPublicKey
from google.cloud.binaryauthorization_v1beta1.types.resources import PkixPublicKey
from google.cloud.binaryauthorization_v1beta1.types.resources import Policy
from google.cloud.binaryauthorization_v1beta1.types.resources import (
    UserOwnedDrydockNote,
)
from google.cloud.binaryauthorization_v1beta1.types.service import CreateAttestorRequest
from google.cloud.binaryauthorization_v1beta1.types.service import DeleteAttestorRequest
from google.cloud.binaryauthorization_v1beta1.types.service import GetAttestorRequest
from google.cloud.binaryauthorization_v1beta1.types.service import GetPolicyRequest
from google.cloud.binaryauthorization_v1beta1.types.service import ListAttestorsRequest
from google.cloud.binaryauthorization_v1beta1.types.service import ListAttestorsResponse
from google.cloud.binaryauthorization_v1beta1.types.service import UpdateAttestorRequest
from google.cloud.binaryauthorization_v1beta1.types.service import UpdatePolicyRequest

__all__ = (
    "AdmissionRule",
    "AdmissionWhitelistPattern",
    "Attestor",
    "AttestorPublicKey",
    "BinauthzManagementServiceV1Beta1AsyncClient",
    "BinauthzManagementServiceV1Beta1Client",
    "CreateAttestorRequest",
    "DeleteAttestorRequest",
    "GetAttestorRequest",
    "GetPolicyRequest",
    "ListAttestorsRequest",
    "ListAttestorsResponse",
    "PkixPublicKey",
    "Policy",
    "UpdateAttestorRequest",
    "UpdatePolicyRequest",
    "UserOwnedDrydockNote",
)
