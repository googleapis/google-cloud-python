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
from google.cloud.confidentialcomputing import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.confidentialcomputing_v1.services.confidential_computing.client import ConfidentialComputingClient
from google.cloud.confidentialcomputing_v1.services.confidential_computing.async_client import ConfidentialComputingAsyncClient

from google.cloud.confidentialcomputing_v1.types.service import AwsPrincipalTagsOptions
from google.cloud.confidentialcomputing_v1.types.service import Challenge
from google.cloud.confidentialcomputing_v1.types.service import ConfidentialSpaceInfo
from google.cloud.confidentialcomputing_v1.types.service import ContainerImageSignature
from google.cloud.confidentialcomputing_v1.types.service import CreateChallengeRequest
from google.cloud.confidentialcomputing_v1.types.service import GceShieldedIdentity
from google.cloud.confidentialcomputing_v1.types.service import GcpCredentials
from google.cloud.confidentialcomputing_v1.types.service import SevSnpAttestation
from google.cloud.confidentialcomputing_v1.types.service import SignedEntity
from google.cloud.confidentialcomputing_v1.types.service import TdxCcelAttestation
from google.cloud.confidentialcomputing_v1.types.service import TokenOptions
from google.cloud.confidentialcomputing_v1.types.service import TpmAttestation
from google.cloud.confidentialcomputing_v1.types.service import VerifyAttestationRequest
from google.cloud.confidentialcomputing_v1.types.service import VerifyAttestationResponse
from google.cloud.confidentialcomputing_v1.types.service import VerifyConfidentialGkeRequest
from google.cloud.confidentialcomputing_v1.types.service import VerifyConfidentialGkeResponse
from google.cloud.confidentialcomputing_v1.types.service import VerifyConfidentialSpaceRequest
from google.cloud.confidentialcomputing_v1.types.service import VerifyConfidentialSpaceResponse
from google.cloud.confidentialcomputing_v1.types.service import SignatureType
from google.cloud.confidentialcomputing_v1.types.service import SigningAlgorithm
from google.cloud.confidentialcomputing_v1.types.service import TokenProfile
from google.cloud.confidentialcomputing_v1.types.service import TokenType

__all__ = ('ConfidentialComputingClient',
    'ConfidentialComputingAsyncClient',
    'AwsPrincipalTagsOptions',
    'Challenge',
    'ConfidentialSpaceInfo',
    'ContainerImageSignature',
    'CreateChallengeRequest',
    'GceShieldedIdentity',
    'GcpCredentials',
    'SevSnpAttestation',
    'SignedEntity',
    'TdxCcelAttestation',
    'TokenOptions',
    'TpmAttestation',
    'VerifyAttestationRequest',
    'VerifyAttestationResponse',
    'VerifyConfidentialGkeRequest',
    'VerifyConfidentialGkeResponse',
    'VerifyConfidentialSpaceRequest',
    'VerifyConfidentialSpaceResponse',
    'SignatureType',
    'SigningAlgorithm',
    'TokenProfile',
    'TokenType',
)
