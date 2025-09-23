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
from google.cloud.gkerecommender import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.gkerecommender_v1.services.gke_inference_quickstart.client import GkeInferenceQuickstartClient
from google.cloud.gkerecommender_v1.services.gke_inference_quickstart.async_client import GkeInferenceQuickstartAsyncClient

from google.cloud.gkerecommender_v1.types.gkerecommender import Amount
from google.cloud.gkerecommender_v1.types.gkerecommender import Cost
from google.cloud.gkerecommender_v1.types.gkerecommender import FetchBenchmarkingDataRequest
from google.cloud.gkerecommender_v1.types.gkerecommender import FetchBenchmarkingDataResponse
from google.cloud.gkerecommender_v1.types.gkerecommender import FetchModelServersRequest
from google.cloud.gkerecommender_v1.types.gkerecommender import FetchModelServersResponse
from google.cloud.gkerecommender_v1.types.gkerecommender import FetchModelServerVersionsRequest
from google.cloud.gkerecommender_v1.types.gkerecommender import FetchModelServerVersionsResponse
from google.cloud.gkerecommender_v1.types.gkerecommender import FetchModelsRequest
from google.cloud.gkerecommender_v1.types.gkerecommender import FetchModelsResponse
from google.cloud.gkerecommender_v1.types.gkerecommender import FetchProfilesRequest
from google.cloud.gkerecommender_v1.types.gkerecommender import FetchProfilesResponse
from google.cloud.gkerecommender_v1.types.gkerecommender import GenerateOptimizedManifestRequest
from google.cloud.gkerecommender_v1.types.gkerecommender import GenerateOptimizedManifestResponse
from google.cloud.gkerecommender_v1.types.gkerecommender import KubernetesManifest
from google.cloud.gkerecommender_v1.types.gkerecommender import MillisecondRange
from google.cloud.gkerecommender_v1.types.gkerecommender import ModelServerInfo
from google.cloud.gkerecommender_v1.types.gkerecommender import PerformanceRange
from google.cloud.gkerecommender_v1.types.gkerecommender import PerformanceRequirements
from google.cloud.gkerecommender_v1.types.gkerecommender import PerformanceStats
from google.cloud.gkerecommender_v1.types.gkerecommender import Profile
from google.cloud.gkerecommender_v1.types.gkerecommender import ResourcesUsed
from google.cloud.gkerecommender_v1.types.gkerecommender import StorageConfig
from google.cloud.gkerecommender_v1.types.gkerecommender import TokensPerSecondRange

__all__ = ('GkeInferenceQuickstartClient',
    'GkeInferenceQuickstartAsyncClient',
    'Amount',
    'Cost',
    'FetchBenchmarkingDataRequest',
    'FetchBenchmarkingDataResponse',
    'FetchModelServersRequest',
    'FetchModelServersResponse',
    'FetchModelServerVersionsRequest',
    'FetchModelServerVersionsResponse',
    'FetchModelsRequest',
    'FetchModelsResponse',
    'FetchProfilesRequest',
    'FetchProfilesResponse',
    'GenerateOptimizedManifestRequest',
    'GenerateOptimizedManifestResponse',
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
