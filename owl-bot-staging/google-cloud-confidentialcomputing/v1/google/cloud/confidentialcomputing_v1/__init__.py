# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.confidentialcomputing_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.confidential_computing import ConfidentialComputingClient
from .services.confidential_computing import ConfidentialComputingAsyncClient

from .types.service import Challenge
from .types.service import ConfidentialSpaceInfo
from .types.service import ContainerImageSignature
from .types.service import CreateChallengeRequest
from .types.service import GcpCredentials
from .types.service import SignedEntity
from .types.service import TokenOptions
from .types.service import TpmAttestation
from .types.service import VerifyAttestationRequest
from .types.service import VerifyAttestationResponse
from .types.service import SigningAlgorithm
from .types.service import TokenType

__all__ = (
    'ConfidentialComputingAsyncClient',
'Challenge',
'ConfidentialComputingClient',
'ConfidentialSpaceInfo',
'ContainerImageSignature',
'CreateChallengeRequest',
'GcpCredentials',
'SignedEntity',
'SigningAlgorithm',
'TokenOptions',
'TokenType',
'TpmAttestation',
'VerifyAttestationRequest',
'VerifyAttestationResponse',
)
