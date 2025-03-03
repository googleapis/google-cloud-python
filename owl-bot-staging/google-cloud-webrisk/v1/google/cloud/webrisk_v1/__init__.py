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
from google.cloud.webrisk_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.web_risk_service import WebRiskServiceClient
from .services.web_risk_service import WebRiskServiceAsyncClient

from .types.webrisk import ComputeThreatListDiffRequest
from .types.webrisk import ComputeThreatListDiffResponse
from .types.webrisk import CreateSubmissionRequest
from .types.webrisk import RawHashes
from .types.webrisk import RawIndices
from .types.webrisk import RiceDeltaEncoding
from .types.webrisk import SearchHashesRequest
from .types.webrisk import SearchHashesResponse
from .types.webrisk import SearchUrisRequest
from .types.webrisk import SearchUrisResponse
from .types.webrisk import Submission
from .types.webrisk import SubmitUriMetadata
from .types.webrisk import SubmitUriRequest
from .types.webrisk import ThreatDiscovery
from .types.webrisk import ThreatEntryAdditions
from .types.webrisk import ThreatEntryRemovals
from .types.webrisk import ThreatInfo
from .types.webrisk import CompressionType
from .types.webrisk import ThreatType

__all__ = (
    'WebRiskServiceAsyncClient',
'CompressionType',
'ComputeThreatListDiffRequest',
'ComputeThreatListDiffResponse',
'CreateSubmissionRequest',
'RawHashes',
'RawIndices',
'RiceDeltaEncoding',
'SearchHashesRequest',
'SearchHashesResponse',
'SearchUrisRequest',
'SearchUrisResponse',
'Submission',
'SubmitUriMetadata',
'SubmitUriRequest',
'ThreatDiscovery',
'ThreatEntryAdditions',
'ThreatEntryRemovals',
'ThreatInfo',
'ThreatType',
'WebRiskServiceClient',
)
