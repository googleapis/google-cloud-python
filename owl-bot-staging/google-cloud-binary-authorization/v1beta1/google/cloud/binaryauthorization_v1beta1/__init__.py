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
from google.cloud.binaryauthorization_v1beta1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.binauthz_management_service_v1_beta1 import BinauthzManagementServiceV1Beta1Client
from .services.binauthz_management_service_v1_beta1 import BinauthzManagementServiceV1Beta1AsyncClient
from .services.system_policy_v1_beta1 import SystemPolicyV1Beta1Client
from .services.system_policy_v1_beta1 import SystemPolicyV1Beta1AsyncClient

from .types.continuous_validation_logging import ContinuousValidationEvent
from .types.resources import AdmissionRule
from .types.resources import AdmissionWhitelistPattern
from .types.resources import Attestor
from .types.resources import AttestorPublicKey
from .types.resources import PkixPublicKey
from .types.resources import Policy
from .types.resources import UserOwnedDrydockNote
from .types.service import CreateAttestorRequest
from .types.service import DeleteAttestorRequest
from .types.service import GetAttestorRequest
from .types.service import GetPolicyRequest
from .types.service import GetSystemPolicyRequest
from .types.service import ListAttestorsRequest
from .types.service import ListAttestorsResponse
from .types.service import UpdateAttestorRequest
from .types.service import UpdatePolicyRequest

__all__ = (
    'BinauthzManagementServiceV1Beta1AsyncClient',
    'SystemPolicyV1Beta1AsyncClient',
'AdmissionRule',
'AdmissionWhitelistPattern',
'Attestor',
'AttestorPublicKey',
'BinauthzManagementServiceV1Beta1Client',
'ContinuousValidationEvent',
'CreateAttestorRequest',
'DeleteAttestorRequest',
'GetAttestorRequest',
'GetPolicyRequest',
'GetSystemPolicyRequest',
'ListAttestorsRequest',
'ListAttestorsResponse',
'PkixPublicKey',
'Policy',
'SystemPolicyV1Beta1Client',
'UpdateAttestorRequest',
'UpdatePolicyRequest',
'UserOwnedDrydockNote',
)
