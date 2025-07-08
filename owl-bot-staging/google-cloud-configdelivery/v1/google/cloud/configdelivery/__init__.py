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
from google.cloud.configdelivery import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.configdelivery_v1.services.config_delivery.client import ConfigDeliveryClient
from google.cloud.configdelivery_v1.services.config_delivery.async_client import ConfigDeliveryAsyncClient

from google.cloud.configdelivery_v1.types.config_delivery import AbortRolloutRequest
from google.cloud.configdelivery_v1.types.config_delivery import AllAtOnceStrategy
from google.cloud.configdelivery_v1.types.config_delivery import AllAtOnceStrategyInfo
from google.cloud.configdelivery_v1.types.config_delivery import ClusterInfo
from google.cloud.configdelivery_v1.types.config_delivery import CreateFleetPackageRequest
from google.cloud.configdelivery_v1.types.config_delivery import CreateReleaseRequest
from google.cloud.configdelivery_v1.types.config_delivery import CreateResourceBundleRequest
from google.cloud.configdelivery_v1.types.config_delivery import CreateVariantRequest
from google.cloud.configdelivery_v1.types.config_delivery import DeleteFleetPackageRequest
from google.cloud.configdelivery_v1.types.config_delivery import DeleteReleaseRequest
from google.cloud.configdelivery_v1.types.config_delivery import DeleteResourceBundleRequest
from google.cloud.configdelivery_v1.types.config_delivery import DeleteVariantRequest
from google.cloud.configdelivery_v1.types.config_delivery import Fleet
from google.cloud.configdelivery_v1.types.config_delivery import FleetPackage
from google.cloud.configdelivery_v1.types.config_delivery import FleetPackageError
from google.cloud.configdelivery_v1.types.config_delivery import FleetPackageInfo
from google.cloud.configdelivery_v1.types.config_delivery import GetFleetPackageRequest
from google.cloud.configdelivery_v1.types.config_delivery import GetReleaseRequest
from google.cloud.configdelivery_v1.types.config_delivery import GetResourceBundleRequest
from google.cloud.configdelivery_v1.types.config_delivery import GetRolloutRequest
from google.cloud.configdelivery_v1.types.config_delivery import GetVariantRequest
from google.cloud.configdelivery_v1.types.config_delivery import ListFleetPackagesRequest
from google.cloud.configdelivery_v1.types.config_delivery import ListFleetPackagesResponse
from google.cloud.configdelivery_v1.types.config_delivery import ListReleasesRequest
from google.cloud.configdelivery_v1.types.config_delivery import ListReleasesResponse
from google.cloud.configdelivery_v1.types.config_delivery import ListResourceBundlesRequest
from google.cloud.configdelivery_v1.types.config_delivery import ListResourceBundlesResponse
from google.cloud.configdelivery_v1.types.config_delivery import ListRolloutsRequest
from google.cloud.configdelivery_v1.types.config_delivery import ListRolloutsResponse
from google.cloud.configdelivery_v1.types.config_delivery import ListVariantsRequest
from google.cloud.configdelivery_v1.types.config_delivery import ListVariantsResponse
from google.cloud.configdelivery_v1.types.config_delivery import OperationMetadata
from google.cloud.configdelivery_v1.types.config_delivery import Release
from google.cloud.configdelivery_v1.types.config_delivery import ReleaseInfo
from google.cloud.configdelivery_v1.types.config_delivery import ResourceBundle
from google.cloud.configdelivery_v1.types.config_delivery import ResourceBundleDeploymentInfo
from google.cloud.configdelivery_v1.types.config_delivery import ResumeRolloutRequest
from google.cloud.configdelivery_v1.types.config_delivery import RollingStrategy
from google.cloud.configdelivery_v1.types.config_delivery import RollingStrategyInfo
from google.cloud.configdelivery_v1.types.config_delivery import Rollout
from google.cloud.configdelivery_v1.types.config_delivery import RolloutInfo
from google.cloud.configdelivery_v1.types.config_delivery import RolloutStrategy
from google.cloud.configdelivery_v1.types.config_delivery import RolloutStrategyInfo
from google.cloud.configdelivery_v1.types.config_delivery import SuspendRolloutRequest
from google.cloud.configdelivery_v1.types.config_delivery import UpdateFleetPackageRequest
from google.cloud.configdelivery_v1.types.config_delivery import UpdateReleaseRequest
from google.cloud.configdelivery_v1.types.config_delivery import UpdateResourceBundleRequest
from google.cloud.configdelivery_v1.types.config_delivery import UpdateVariantRequest
from google.cloud.configdelivery_v1.types.config_delivery import Variant
from google.cloud.configdelivery_v1.types.config_delivery import DeletionPropagationPolicy

__all__ = ('ConfigDeliveryClient',
    'ConfigDeliveryAsyncClient',
    'AbortRolloutRequest',
    'AllAtOnceStrategy',
    'AllAtOnceStrategyInfo',
    'ClusterInfo',
    'CreateFleetPackageRequest',
    'CreateReleaseRequest',
    'CreateResourceBundleRequest',
    'CreateVariantRequest',
    'DeleteFleetPackageRequest',
    'DeleteReleaseRequest',
    'DeleteResourceBundleRequest',
    'DeleteVariantRequest',
    'Fleet',
    'FleetPackage',
    'FleetPackageError',
    'FleetPackageInfo',
    'GetFleetPackageRequest',
    'GetReleaseRequest',
    'GetResourceBundleRequest',
    'GetRolloutRequest',
    'GetVariantRequest',
    'ListFleetPackagesRequest',
    'ListFleetPackagesResponse',
    'ListReleasesRequest',
    'ListReleasesResponse',
    'ListResourceBundlesRequest',
    'ListResourceBundlesResponse',
    'ListRolloutsRequest',
    'ListRolloutsResponse',
    'ListVariantsRequest',
    'ListVariantsResponse',
    'OperationMetadata',
    'Release',
    'ReleaseInfo',
    'ResourceBundle',
    'ResourceBundleDeploymentInfo',
    'ResumeRolloutRequest',
    'RollingStrategy',
    'RollingStrategyInfo',
    'Rollout',
    'RolloutInfo',
    'RolloutStrategy',
    'RolloutStrategyInfo',
    'SuspendRolloutRequest',
    'UpdateFleetPackageRequest',
    'UpdateReleaseRequest',
    'UpdateResourceBundleRequest',
    'UpdateVariantRequest',
    'Variant',
    'DeletionPropagationPolicy',
)
