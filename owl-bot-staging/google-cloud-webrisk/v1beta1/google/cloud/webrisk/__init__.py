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
from google.cloud.webrisk import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.webrisk_v1beta1.services.web_risk_service_v1_beta1.client import WebRiskServiceV1Beta1Client
from google.cloud.webrisk_v1beta1.services.web_risk_service_v1_beta1.async_client import WebRiskServiceV1Beta1AsyncClient

from google.cloud.webrisk_v1beta1.types.webrisk import ComputeThreatListDiffRequest
from google.cloud.webrisk_v1beta1.types.webrisk import ComputeThreatListDiffResponse
from google.cloud.webrisk_v1beta1.types.webrisk import RawHashes
from google.cloud.webrisk_v1beta1.types.webrisk import RawIndices
from google.cloud.webrisk_v1beta1.types.webrisk import RiceDeltaEncoding
from google.cloud.webrisk_v1beta1.types.webrisk import SearchHashesRequest
from google.cloud.webrisk_v1beta1.types.webrisk import SearchHashesResponse
from google.cloud.webrisk_v1beta1.types.webrisk import SearchUrisRequest
from google.cloud.webrisk_v1beta1.types.webrisk import SearchUrisResponse
from google.cloud.webrisk_v1beta1.types.webrisk import ThreatEntryAdditions
from google.cloud.webrisk_v1beta1.types.webrisk import ThreatEntryRemovals
from google.cloud.webrisk_v1beta1.types.webrisk import CompressionType
from google.cloud.webrisk_v1beta1.types.webrisk import ThreatType

__all__ = ('WebRiskServiceV1Beta1Client',
    'WebRiskServiceV1Beta1AsyncClient',
    'ComputeThreatListDiffRequest',
    'ComputeThreatListDiffResponse',
    'RawHashes',
    'RawIndices',
    'RiceDeltaEncoding',
    'SearchHashesRequest',
    'SearchHashesResponse',
    'SearchUrisRequest',
    'SearchUrisResponse',
    'ThreatEntryAdditions',
    'ThreatEntryRemovals',
    'CompressionType',
    'ThreatType',
)
