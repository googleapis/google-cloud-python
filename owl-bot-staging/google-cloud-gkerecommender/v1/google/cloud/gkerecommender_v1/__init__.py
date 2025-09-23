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
from google.cloud.gkerecommender_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.gke_inference_quickstart import GkeInferenceQuickstartClient
from .services.gke_inference_quickstart import GkeInferenceQuickstartAsyncClient

from .types.gkerecommender import Amount
from .types.gkerecommender import Cost
from .types.gkerecommender import FetchBenchmarkingDataRequest
from .types.gkerecommender import FetchBenchmarkingDataResponse
from .types.gkerecommender import FetchModelServersRequest
from .types.gkerecommender import FetchModelServersResponse
from .types.gkerecommender import FetchModelServerVersionsRequest
from .types.gkerecommender import FetchModelServerVersionsResponse
from .types.gkerecommender import FetchModelsRequest
from .types.gkerecommender import FetchModelsResponse
from .types.gkerecommender import FetchProfilesRequest
from .types.gkerecommender import FetchProfilesResponse
from .types.gkerecommender import GenerateOptimizedManifestRequest
from .types.gkerecommender import GenerateOptimizedManifestResponse
from .types.gkerecommender import KubernetesManifest
from .types.gkerecommender import MillisecondRange
from .types.gkerecommender import ModelServerInfo
from .types.gkerecommender import PerformanceRange
from .types.gkerecommender import PerformanceRequirements
from .types.gkerecommender import PerformanceStats
from .types.gkerecommender import Profile
from .types.gkerecommender import ResourcesUsed
from .types.gkerecommender import StorageConfig
from .types.gkerecommender import TokensPerSecondRange

__all__ = (
    'GkeInferenceQuickstartAsyncClient',
'Amount',
'Cost',
'FetchBenchmarkingDataRequest',
'FetchBenchmarkingDataResponse',
'FetchModelServerVersionsRequest',
'FetchModelServerVersionsResponse',
'FetchModelServersRequest',
'FetchModelServersResponse',
'FetchModelsRequest',
'FetchModelsResponse',
'FetchProfilesRequest',
'FetchProfilesResponse',
'GenerateOptimizedManifestRequest',
'GenerateOptimizedManifestResponse',
'GkeInferenceQuickstartClient',
'KubernetesManifest',
'MillisecondRange',
'ModelServerInfo',
'PerformanceRange',
'PerformanceRequirements',
'PerformanceStats',
'Profile',
'ResourcesUsed',
'StorageConfig',
'TokensPerSecondRange',
)
