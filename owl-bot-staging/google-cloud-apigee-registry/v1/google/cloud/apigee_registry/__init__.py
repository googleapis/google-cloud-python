# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.cloud.apigee_registry import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.apigee_registry_v1.services.provisioning.client import ProvisioningClient
from google.cloud.apigee_registry_v1.services.provisioning.async_client import ProvisioningAsyncClient
from google.cloud.apigee_registry_v1.services.registry.client import RegistryClient
from google.cloud.apigee_registry_v1.services.registry.async_client import RegistryAsyncClient

from google.cloud.apigee_registry_v1.types.provisioning_service import CreateInstanceRequest
from google.cloud.apigee_registry_v1.types.provisioning_service import DeleteInstanceRequest
from google.cloud.apigee_registry_v1.types.provisioning_service import GetInstanceRequest
from google.cloud.apigee_registry_v1.types.provisioning_service import Instance
from google.cloud.apigee_registry_v1.types.provisioning_service import OperationMetadata
from google.cloud.apigee_registry_v1.types.registry_models import Api
from google.cloud.apigee_registry_v1.types.registry_models import ApiDeployment
from google.cloud.apigee_registry_v1.types.registry_models import ApiSpec
from google.cloud.apigee_registry_v1.types.registry_models import ApiVersion
from google.cloud.apigee_registry_v1.types.registry_models import Artifact
from google.cloud.apigee_registry_v1.types.registry_service import CreateApiDeploymentRequest
from google.cloud.apigee_registry_v1.types.registry_service import CreateApiRequest
from google.cloud.apigee_registry_v1.types.registry_service import CreateApiSpecRequest
from google.cloud.apigee_registry_v1.types.registry_service import CreateApiVersionRequest
from google.cloud.apigee_registry_v1.types.registry_service import CreateArtifactRequest
from google.cloud.apigee_registry_v1.types.registry_service import DeleteApiDeploymentRequest
from google.cloud.apigee_registry_v1.types.registry_service import DeleteApiDeploymentRevisionRequest
from google.cloud.apigee_registry_v1.types.registry_service import DeleteApiRequest
from google.cloud.apigee_registry_v1.types.registry_service import DeleteApiSpecRequest
from google.cloud.apigee_registry_v1.types.registry_service import DeleteApiSpecRevisionRequest
from google.cloud.apigee_registry_v1.types.registry_service import DeleteApiVersionRequest
from google.cloud.apigee_registry_v1.types.registry_service import DeleteArtifactRequest
from google.cloud.apigee_registry_v1.types.registry_service import GetApiDeploymentRequest
from google.cloud.apigee_registry_v1.types.registry_service import GetApiRequest
from google.cloud.apigee_registry_v1.types.registry_service import GetApiSpecContentsRequest
from google.cloud.apigee_registry_v1.types.registry_service import GetApiSpecRequest
from google.cloud.apigee_registry_v1.types.registry_service import GetApiVersionRequest
from google.cloud.apigee_registry_v1.types.registry_service import GetArtifactContentsRequest
from google.cloud.apigee_registry_v1.types.registry_service import GetArtifactRequest
from google.cloud.apigee_registry_v1.types.registry_service import ListApiDeploymentRevisionsRequest
from google.cloud.apigee_registry_v1.types.registry_service import ListApiDeploymentRevisionsResponse
from google.cloud.apigee_registry_v1.types.registry_service import ListApiDeploymentsRequest
from google.cloud.apigee_registry_v1.types.registry_service import ListApiDeploymentsResponse
from google.cloud.apigee_registry_v1.types.registry_service import ListApiSpecRevisionsRequest
from google.cloud.apigee_registry_v1.types.registry_service import ListApiSpecRevisionsResponse
from google.cloud.apigee_registry_v1.types.registry_service import ListApiSpecsRequest
from google.cloud.apigee_registry_v1.types.registry_service import ListApiSpecsResponse
from google.cloud.apigee_registry_v1.types.registry_service import ListApisRequest
from google.cloud.apigee_registry_v1.types.registry_service import ListApisResponse
from google.cloud.apigee_registry_v1.types.registry_service import ListApiVersionsRequest
from google.cloud.apigee_registry_v1.types.registry_service import ListApiVersionsResponse
from google.cloud.apigee_registry_v1.types.registry_service import ListArtifactsRequest
from google.cloud.apigee_registry_v1.types.registry_service import ListArtifactsResponse
from google.cloud.apigee_registry_v1.types.registry_service import ReplaceArtifactRequest
from google.cloud.apigee_registry_v1.types.registry_service import RollbackApiDeploymentRequest
from google.cloud.apigee_registry_v1.types.registry_service import RollbackApiSpecRequest
from google.cloud.apigee_registry_v1.types.registry_service import TagApiDeploymentRevisionRequest
from google.cloud.apigee_registry_v1.types.registry_service import TagApiSpecRevisionRequest
from google.cloud.apigee_registry_v1.types.registry_service import UpdateApiDeploymentRequest
from google.cloud.apigee_registry_v1.types.registry_service import UpdateApiRequest
from google.cloud.apigee_registry_v1.types.registry_service import UpdateApiSpecRequest
from google.cloud.apigee_registry_v1.types.registry_service import UpdateApiVersionRequest

__all__ = ('ProvisioningClient',
    'ProvisioningAsyncClient',
    'RegistryClient',
    'RegistryAsyncClient',
    'CreateInstanceRequest',
    'DeleteInstanceRequest',
    'GetInstanceRequest',
    'Instance',
    'OperationMetadata',
    'Api',
    'ApiDeployment',
    'ApiSpec',
    'ApiVersion',
    'Artifact',
    'CreateApiDeploymentRequest',
    'CreateApiRequest',
    'CreateApiSpecRequest',
    'CreateApiVersionRequest',
    'CreateArtifactRequest',
    'DeleteApiDeploymentRequest',
    'DeleteApiDeploymentRevisionRequest',
    'DeleteApiRequest',
    'DeleteApiSpecRequest',
    'DeleteApiSpecRevisionRequest',
    'DeleteApiVersionRequest',
    'DeleteArtifactRequest',
    'GetApiDeploymentRequest',
    'GetApiRequest',
    'GetApiSpecContentsRequest',
    'GetApiSpecRequest',
    'GetApiVersionRequest',
    'GetArtifactContentsRequest',
    'GetArtifactRequest',
    'ListApiDeploymentRevisionsRequest',
    'ListApiDeploymentRevisionsResponse',
    'ListApiDeploymentsRequest',
    'ListApiDeploymentsResponse',
    'ListApiSpecRevisionsRequest',
    'ListApiSpecRevisionsResponse',
    'ListApiSpecsRequest',
    'ListApiSpecsResponse',
    'ListApisRequest',
    'ListApisResponse',
    'ListApiVersionsRequest',
    'ListApiVersionsResponse',
    'ListArtifactsRequest',
    'ListArtifactsResponse',
    'ReplaceArtifactRequest',
    'RollbackApiDeploymentRequest',
    'RollbackApiSpecRequest',
    'TagApiDeploymentRevisionRequest',
    'TagApiSpecRevisionRequest',
    'UpdateApiDeploymentRequest',
    'UpdateApiRequest',
    'UpdateApiSpecRequest',
    'UpdateApiVersionRequest',
)
