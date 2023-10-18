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
from google.cloud.config import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.config_v1.services.config.client import ConfigClient
from google.cloud.config_v1.services.config.async_client import ConfigAsyncClient

from google.cloud.config_v1.types.config import ApplyResults
from google.cloud.config_v1.types.config import CreateDeploymentRequest
from google.cloud.config_v1.types.config import DeleteDeploymentRequest
from google.cloud.config_v1.types.config import DeleteStatefileRequest
from google.cloud.config_v1.types.config import Deployment
from google.cloud.config_v1.types.config import DeploymentOperationMetadata
from google.cloud.config_v1.types.config import ExportDeploymentStatefileRequest
from google.cloud.config_v1.types.config import ExportLockInfoRequest
from google.cloud.config_v1.types.config import ExportRevisionStatefileRequest
from google.cloud.config_v1.types.config import GetDeploymentRequest
from google.cloud.config_v1.types.config import GetResourceRequest
from google.cloud.config_v1.types.config import GetRevisionRequest
from google.cloud.config_v1.types.config import GitSource
from google.cloud.config_v1.types.config import ImportStatefileRequest
from google.cloud.config_v1.types.config import ListDeploymentsRequest
from google.cloud.config_v1.types.config import ListDeploymentsResponse
from google.cloud.config_v1.types.config import ListResourcesRequest
from google.cloud.config_v1.types.config import ListResourcesResponse
from google.cloud.config_v1.types.config import ListRevisionsRequest
from google.cloud.config_v1.types.config import ListRevisionsResponse
from google.cloud.config_v1.types.config import LockDeploymentRequest
from google.cloud.config_v1.types.config import LockInfo
from google.cloud.config_v1.types.config import OperationMetadata
from google.cloud.config_v1.types.config import Resource
from google.cloud.config_v1.types.config import ResourceCAIInfo
from google.cloud.config_v1.types.config import ResourceTerraformInfo
from google.cloud.config_v1.types.config import Revision
from google.cloud.config_v1.types.config import Statefile
from google.cloud.config_v1.types.config import TerraformBlueprint
from google.cloud.config_v1.types.config import TerraformError
from google.cloud.config_v1.types.config import TerraformOutput
from google.cloud.config_v1.types.config import TerraformVariable
from google.cloud.config_v1.types.config import UnlockDeploymentRequest
from google.cloud.config_v1.types.config import UpdateDeploymentRequest

__all__ = ('ConfigClient',
    'ConfigAsyncClient',
    'ApplyResults',
    'CreateDeploymentRequest',
    'DeleteDeploymentRequest',
    'DeleteStatefileRequest',
    'Deployment',
    'DeploymentOperationMetadata',
    'ExportDeploymentStatefileRequest',
    'ExportLockInfoRequest',
    'ExportRevisionStatefileRequest',
    'GetDeploymentRequest',
    'GetResourceRequest',
    'GetRevisionRequest',
    'GitSource',
    'ImportStatefileRequest',
    'ListDeploymentsRequest',
    'ListDeploymentsResponse',
    'ListResourcesRequest',
    'ListResourcesResponse',
    'ListRevisionsRequest',
    'ListRevisionsResponse',
    'LockDeploymentRequest',
    'LockInfo',
    'OperationMetadata',
    'Resource',
    'ResourceCAIInfo',
    'ResourceTerraformInfo',
    'Revision',
    'Statefile',
    'TerraformBlueprint',
    'TerraformError',
    'TerraformOutput',
    'TerraformVariable',
    'UnlockDeploymentRequest',
    'UpdateDeploymentRequest',
)
