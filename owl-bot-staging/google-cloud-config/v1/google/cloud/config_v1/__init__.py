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
from google.cloud.config_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.config import ConfigClient
from .services.config import ConfigAsyncClient

from .types.config import ApplyResults
from .types.config import CreateDeploymentRequest
from .types.config import DeleteDeploymentRequest
from .types.config import DeleteStatefileRequest
from .types.config import Deployment
from .types.config import DeploymentOperationMetadata
from .types.config import ExportDeploymentStatefileRequest
from .types.config import ExportLockInfoRequest
from .types.config import ExportRevisionStatefileRequest
from .types.config import GetDeploymentRequest
from .types.config import GetResourceRequest
from .types.config import GetRevisionRequest
from .types.config import GitSource
from .types.config import ImportStatefileRequest
from .types.config import ListDeploymentsRequest
from .types.config import ListDeploymentsResponse
from .types.config import ListResourcesRequest
from .types.config import ListResourcesResponse
from .types.config import ListRevisionsRequest
from .types.config import ListRevisionsResponse
from .types.config import LockDeploymentRequest
from .types.config import LockInfo
from .types.config import OperationMetadata
from .types.config import Resource
from .types.config import ResourceCAIInfo
from .types.config import ResourceTerraformInfo
from .types.config import Revision
from .types.config import Statefile
from .types.config import TerraformBlueprint
from .types.config import TerraformError
from .types.config import TerraformOutput
from .types.config import TerraformVariable
from .types.config import UnlockDeploymentRequest
from .types.config import UpdateDeploymentRequest

__all__ = (
    'ConfigAsyncClient',
'ApplyResults',
'ConfigClient',
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
