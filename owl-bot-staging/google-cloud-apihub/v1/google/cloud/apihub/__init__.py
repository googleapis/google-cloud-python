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
from google.cloud.apihub import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.apihub_v1.services.api_hub.client import ApiHubClient
from google.cloud.apihub_v1.services.api_hub.async_client import ApiHubAsyncClient
from google.cloud.apihub_v1.services.api_hub_dependencies.client import ApiHubDependenciesClient
from google.cloud.apihub_v1.services.api_hub_dependencies.async_client import ApiHubDependenciesAsyncClient
from google.cloud.apihub_v1.services.api_hub_plugin.client import ApiHubPluginClient
from google.cloud.apihub_v1.services.api_hub_plugin.async_client import ApiHubPluginAsyncClient
from google.cloud.apihub_v1.services.host_project_registration_service.client import HostProjectRegistrationServiceClient
from google.cloud.apihub_v1.services.host_project_registration_service.async_client import HostProjectRegistrationServiceAsyncClient
from google.cloud.apihub_v1.services.linting_service.client import LintingServiceClient
from google.cloud.apihub_v1.services.linting_service.async_client import LintingServiceAsyncClient
from google.cloud.apihub_v1.services.provisioning.client import ProvisioningClient
from google.cloud.apihub_v1.services.provisioning.async_client import ProvisioningAsyncClient
from google.cloud.apihub_v1.services.runtime_project_attachment_service.client import RuntimeProjectAttachmentServiceClient
from google.cloud.apihub_v1.services.runtime_project_attachment_service.async_client import RuntimeProjectAttachmentServiceAsyncClient

from google.cloud.apihub_v1.types.apihub_service import ApiHubResource
from google.cloud.apihub_v1.types.apihub_service import CreateApiRequest
from google.cloud.apihub_v1.types.apihub_service import CreateAttributeRequest
from google.cloud.apihub_v1.types.apihub_service import CreateDependencyRequest
from google.cloud.apihub_v1.types.apihub_service import CreateDeploymentRequest
from google.cloud.apihub_v1.types.apihub_service import CreateExternalApiRequest
from google.cloud.apihub_v1.types.apihub_service import CreateSpecRequest
from google.cloud.apihub_v1.types.apihub_service import CreateVersionRequest
from google.cloud.apihub_v1.types.apihub_service import DeleteApiRequest
from google.cloud.apihub_v1.types.apihub_service import DeleteAttributeRequest
from google.cloud.apihub_v1.types.apihub_service import DeleteDependencyRequest
from google.cloud.apihub_v1.types.apihub_service import DeleteDeploymentRequest
from google.cloud.apihub_v1.types.apihub_service import DeleteExternalApiRequest
from google.cloud.apihub_v1.types.apihub_service import DeleteSpecRequest
from google.cloud.apihub_v1.types.apihub_service import DeleteVersionRequest
from google.cloud.apihub_v1.types.apihub_service import GetApiOperationRequest
from google.cloud.apihub_v1.types.apihub_service import GetApiRequest
from google.cloud.apihub_v1.types.apihub_service import GetAttributeRequest
from google.cloud.apihub_v1.types.apihub_service import GetDefinitionRequest
from google.cloud.apihub_v1.types.apihub_service import GetDependencyRequest
from google.cloud.apihub_v1.types.apihub_service import GetDeploymentRequest
from google.cloud.apihub_v1.types.apihub_service import GetExternalApiRequest
from google.cloud.apihub_v1.types.apihub_service import GetSpecContentsRequest
from google.cloud.apihub_v1.types.apihub_service import GetSpecRequest
from google.cloud.apihub_v1.types.apihub_service import GetVersionRequest
from google.cloud.apihub_v1.types.apihub_service import ListApiOperationsRequest
from google.cloud.apihub_v1.types.apihub_service import ListApiOperationsResponse
from google.cloud.apihub_v1.types.apihub_service import ListApisRequest
from google.cloud.apihub_v1.types.apihub_service import ListApisResponse
from google.cloud.apihub_v1.types.apihub_service import ListAttributesRequest
from google.cloud.apihub_v1.types.apihub_service import ListAttributesResponse
from google.cloud.apihub_v1.types.apihub_service import ListDependenciesRequest
from google.cloud.apihub_v1.types.apihub_service import ListDependenciesResponse
from google.cloud.apihub_v1.types.apihub_service import ListDeploymentsRequest
from google.cloud.apihub_v1.types.apihub_service import ListDeploymentsResponse
from google.cloud.apihub_v1.types.apihub_service import ListExternalApisRequest
from google.cloud.apihub_v1.types.apihub_service import ListExternalApisResponse
from google.cloud.apihub_v1.types.apihub_service import ListSpecsRequest
from google.cloud.apihub_v1.types.apihub_service import ListSpecsResponse
from google.cloud.apihub_v1.types.apihub_service import ListVersionsRequest
from google.cloud.apihub_v1.types.apihub_service import ListVersionsResponse
from google.cloud.apihub_v1.types.apihub_service import SearchResourcesRequest
from google.cloud.apihub_v1.types.apihub_service import SearchResourcesResponse
from google.cloud.apihub_v1.types.apihub_service import SearchResult
from google.cloud.apihub_v1.types.apihub_service import UpdateApiRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateAttributeRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateDependencyRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateDeploymentRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateExternalApiRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateSpecRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateVersionRequest
from google.cloud.apihub_v1.types.common_fields import Api
from google.cloud.apihub_v1.types.common_fields import ApiHubInstance
from google.cloud.apihub_v1.types.common_fields import ApiOperation
from google.cloud.apihub_v1.types.common_fields import Attribute
from google.cloud.apihub_v1.types.common_fields import AttributeValues
from google.cloud.apihub_v1.types.common_fields import Definition
from google.cloud.apihub_v1.types.common_fields import Dependency
from google.cloud.apihub_v1.types.common_fields import DependencyEntityReference
from google.cloud.apihub_v1.types.common_fields import DependencyErrorDetail
from google.cloud.apihub_v1.types.common_fields import Deployment
from google.cloud.apihub_v1.types.common_fields import Documentation
from google.cloud.apihub_v1.types.common_fields import ExternalApi
from google.cloud.apihub_v1.types.common_fields import HttpOperation
from google.cloud.apihub_v1.types.common_fields import Issue
from google.cloud.apihub_v1.types.common_fields import LintResponse
from google.cloud.apihub_v1.types.common_fields import OpenApiSpecDetails
from google.cloud.apihub_v1.types.common_fields import OperationDetails
from google.cloud.apihub_v1.types.common_fields import OperationMetadata
from google.cloud.apihub_v1.types.common_fields import Owner
from google.cloud.apihub_v1.types.common_fields import Path
from google.cloud.apihub_v1.types.common_fields import Point
from google.cloud.apihub_v1.types.common_fields import Range
from google.cloud.apihub_v1.types.common_fields import Schema
from google.cloud.apihub_v1.types.common_fields import Spec
from google.cloud.apihub_v1.types.common_fields import SpecContents
from google.cloud.apihub_v1.types.common_fields import SpecDetails
from google.cloud.apihub_v1.types.common_fields import Version
from google.cloud.apihub_v1.types.common_fields import Linter
from google.cloud.apihub_v1.types.common_fields import LintState
from google.cloud.apihub_v1.types.common_fields import Severity
from google.cloud.apihub_v1.types.host_project_registration_service import CreateHostProjectRegistrationRequest
from google.cloud.apihub_v1.types.host_project_registration_service import GetHostProjectRegistrationRequest
from google.cloud.apihub_v1.types.host_project_registration_service import HostProjectRegistration
from google.cloud.apihub_v1.types.host_project_registration_service import ListHostProjectRegistrationsRequest
from google.cloud.apihub_v1.types.host_project_registration_service import ListHostProjectRegistrationsResponse
from google.cloud.apihub_v1.types.linting_service import GetStyleGuideContentsRequest
from google.cloud.apihub_v1.types.linting_service import GetStyleGuideRequest
from google.cloud.apihub_v1.types.linting_service import LintSpecRequest
from google.cloud.apihub_v1.types.linting_service import StyleGuide
from google.cloud.apihub_v1.types.linting_service import StyleGuideContents
from google.cloud.apihub_v1.types.linting_service import UpdateStyleGuideRequest
from google.cloud.apihub_v1.types.plugin_service import DisablePluginRequest
from google.cloud.apihub_v1.types.plugin_service import EnablePluginRequest
from google.cloud.apihub_v1.types.plugin_service import GetPluginRequest
from google.cloud.apihub_v1.types.plugin_service import Plugin
from google.cloud.apihub_v1.types.provisioning_service import CreateApiHubInstanceRequest
from google.cloud.apihub_v1.types.provisioning_service import GetApiHubInstanceRequest
from google.cloud.apihub_v1.types.provisioning_service import LookupApiHubInstanceRequest
from google.cloud.apihub_v1.types.provisioning_service import LookupApiHubInstanceResponse
from google.cloud.apihub_v1.types.runtime_project_attachment_service import CreateRuntimeProjectAttachmentRequest
from google.cloud.apihub_v1.types.runtime_project_attachment_service import DeleteRuntimeProjectAttachmentRequest
from google.cloud.apihub_v1.types.runtime_project_attachment_service import GetRuntimeProjectAttachmentRequest
from google.cloud.apihub_v1.types.runtime_project_attachment_service import ListRuntimeProjectAttachmentsRequest
from google.cloud.apihub_v1.types.runtime_project_attachment_service import ListRuntimeProjectAttachmentsResponse
from google.cloud.apihub_v1.types.runtime_project_attachment_service import LookupRuntimeProjectAttachmentRequest
from google.cloud.apihub_v1.types.runtime_project_attachment_service import LookupRuntimeProjectAttachmentResponse
from google.cloud.apihub_v1.types.runtime_project_attachment_service import RuntimeProjectAttachment

__all__ = ('ApiHubClient',
    'ApiHubAsyncClient',
    'ApiHubDependenciesClient',
    'ApiHubDependenciesAsyncClient',
    'ApiHubPluginClient',
    'ApiHubPluginAsyncClient',
    'HostProjectRegistrationServiceClient',
    'HostProjectRegistrationServiceAsyncClient',
    'LintingServiceClient',
    'LintingServiceAsyncClient',
    'ProvisioningClient',
    'ProvisioningAsyncClient',
    'RuntimeProjectAttachmentServiceClient',
    'RuntimeProjectAttachmentServiceAsyncClient',
    'ApiHubResource',
    'CreateApiRequest',
    'CreateAttributeRequest',
    'CreateDependencyRequest',
    'CreateDeploymentRequest',
    'CreateExternalApiRequest',
    'CreateSpecRequest',
    'CreateVersionRequest',
    'DeleteApiRequest',
    'DeleteAttributeRequest',
    'DeleteDependencyRequest',
    'DeleteDeploymentRequest',
    'DeleteExternalApiRequest',
    'DeleteSpecRequest',
    'DeleteVersionRequest',
    'GetApiOperationRequest',
    'GetApiRequest',
    'GetAttributeRequest',
    'GetDefinitionRequest',
    'GetDependencyRequest',
    'GetDeploymentRequest',
    'GetExternalApiRequest',
    'GetSpecContentsRequest',
    'GetSpecRequest',
    'GetVersionRequest',
    'ListApiOperationsRequest',
    'ListApiOperationsResponse',
    'ListApisRequest',
    'ListApisResponse',
    'ListAttributesRequest',
    'ListAttributesResponse',
    'ListDependenciesRequest',
    'ListDependenciesResponse',
    'ListDeploymentsRequest',
    'ListDeploymentsResponse',
    'ListExternalApisRequest',
    'ListExternalApisResponse',
    'ListSpecsRequest',
    'ListSpecsResponse',
    'ListVersionsRequest',
    'ListVersionsResponse',
    'SearchResourcesRequest',
    'SearchResourcesResponse',
    'SearchResult',
    'UpdateApiRequest',
    'UpdateAttributeRequest',
    'UpdateDependencyRequest',
    'UpdateDeploymentRequest',
    'UpdateExternalApiRequest',
    'UpdateSpecRequest',
    'UpdateVersionRequest',
    'Api',
    'ApiHubInstance',
    'ApiOperation',
    'Attribute',
    'AttributeValues',
    'Definition',
    'Dependency',
    'DependencyEntityReference',
    'DependencyErrorDetail',
    'Deployment',
    'Documentation',
    'ExternalApi',
    'HttpOperation',
    'Issue',
    'LintResponse',
    'OpenApiSpecDetails',
    'OperationDetails',
    'OperationMetadata',
    'Owner',
    'Path',
    'Point',
    'Range',
    'Schema',
    'Spec',
    'SpecContents',
    'SpecDetails',
    'Version',
    'Linter',
    'LintState',
    'Severity',
    'CreateHostProjectRegistrationRequest',
    'GetHostProjectRegistrationRequest',
    'HostProjectRegistration',
    'ListHostProjectRegistrationsRequest',
    'ListHostProjectRegistrationsResponse',
    'GetStyleGuideContentsRequest',
    'GetStyleGuideRequest',
    'LintSpecRequest',
    'StyleGuide',
    'StyleGuideContents',
    'UpdateStyleGuideRequest',
    'DisablePluginRequest',
    'EnablePluginRequest',
    'GetPluginRequest',
    'Plugin',
    'CreateApiHubInstanceRequest',
    'GetApiHubInstanceRequest',
    'LookupApiHubInstanceRequest',
    'LookupApiHubInstanceResponse',
    'CreateRuntimeProjectAttachmentRequest',
    'DeleteRuntimeProjectAttachmentRequest',
    'GetRuntimeProjectAttachmentRequest',
    'ListRuntimeProjectAttachmentsRequest',
    'ListRuntimeProjectAttachmentsResponse',
    'LookupRuntimeProjectAttachmentRequest',
    'LookupRuntimeProjectAttachmentResponse',
    'RuntimeProjectAttachment',
)
