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
from google.cloud.configdelivery_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.config_delivery import ConfigDeliveryClient
from .services.config_delivery import ConfigDeliveryAsyncClient

from .types.config_delivery import AbortRolloutRequest
from .types.config_delivery import AllAtOnceStrategy
from .types.config_delivery import AllAtOnceStrategyInfo
from .types.config_delivery import ClusterInfo
from .types.config_delivery import CreateFleetPackageRequest
from .types.config_delivery import CreateReleaseRequest
from .types.config_delivery import CreateResourceBundleRequest
from .types.config_delivery import CreateVariantRequest
from .types.config_delivery import DeleteFleetPackageRequest
from .types.config_delivery import DeleteReleaseRequest
from .types.config_delivery import DeleteResourceBundleRequest
from .types.config_delivery import DeleteVariantRequest
from .types.config_delivery import Fleet
from .types.config_delivery import FleetPackage
from .types.config_delivery import FleetPackageError
from .types.config_delivery import FleetPackageInfo
from .types.config_delivery import GetFleetPackageRequest
from .types.config_delivery import GetReleaseRequest
from .types.config_delivery import GetResourceBundleRequest
from .types.config_delivery import GetRolloutRequest
from .types.config_delivery import GetVariantRequest
from .types.config_delivery import ListFleetPackagesRequest
from .types.config_delivery import ListFleetPackagesResponse
from .types.config_delivery import ListReleasesRequest
from .types.config_delivery import ListReleasesResponse
from .types.config_delivery import ListResourceBundlesRequest
from .types.config_delivery import ListResourceBundlesResponse
from .types.config_delivery import ListRolloutsRequest
from .types.config_delivery import ListRolloutsResponse
from .types.config_delivery import ListVariantsRequest
from .types.config_delivery import ListVariantsResponse
from .types.config_delivery import OperationMetadata
from .types.config_delivery import Release
from .types.config_delivery import ReleaseInfo
from .types.config_delivery import ResourceBundle
from .types.config_delivery import ResourceBundleDeploymentInfo
from .types.config_delivery import ResumeRolloutRequest
from .types.config_delivery import RollingStrategy
from .types.config_delivery import RollingStrategyInfo
from .types.config_delivery import Rollout
from .types.config_delivery import RolloutInfo
from .types.config_delivery import RolloutStrategy
from .types.config_delivery import RolloutStrategyInfo
from .types.config_delivery import SuspendRolloutRequest
from .types.config_delivery import UpdateFleetPackageRequest
from .types.config_delivery import UpdateReleaseRequest
from .types.config_delivery import UpdateResourceBundleRequest
from .types.config_delivery import UpdateVariantRequest
from .types.config_delivery import Variant
from .types.config_delivery import DeletionPropagationPolicy

__all__ = (
    'ConfigDeliveryAsyncClient',
'AbortRolloutRequest',
'AllAtOnceStrategy',
'AllAtOnceStrategyInfo',
'ClusterInfo',
'ConfigDeliveryClient',
'CreateFleetPackageRequest',
'CreateReleaseRequest',
'CreateResourceBundleRequest',
'CreateVariantRequest',
'DeleteFleetPackageRequest',
'DeleteReleaseRequest',
'DeleteResourceBundleRequest',
'DeleteVariantRequest',
'DeletionPropagationPolicy',
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
)
