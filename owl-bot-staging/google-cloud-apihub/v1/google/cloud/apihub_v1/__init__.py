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
from google.cloud.apihub_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.api_hub import ApiHubClient
from .services.api_hub import ApiHubAsyncClient
from .services.api_hub_dependencies import ApiHubDependenciesClient
from .services.api_hub_dependencies import ApiHubDependenciesAsyncClient
from .services.api_hub_plugin import ApiHubPluginClient
from .services.api_hub_plugin import ApiHubPluginAsyncClient
from .services.host_project_registration_service import HostProjectRegistrationServiceClient
from .services.host_project_registration_service import HostProjectRegistrationServiceAsyncClient
from .services.linting_service import LintingServiceClient
from .services.linting_service import LintingServiceAsyncClient
from .services.provisioning import ProvisioningClient
from .services.provisioning import ProvisioningAsyncClient
from .services.runtime_project_attachment_service import RuntimeProjectAttachmentServiceClient
from .services.runtime_project_attachment_service import RuntimeProjectAttachmentServiceAsyncClient

from .types.apihub_service import ApiHubResource
from .types.apihub_service import CreateApiRequest
from .types.apihub_service import CreateAttributeRequest
from .types.apihub_service import CreateDependencyRequest
from .types.apihub_service import CreateDeploymentRequest
from .types.apihub_service import CreateExternalApiRequest
from .types.apihub_service import CreateSpecRequest
from .types.apihub_service import CreateVersionRequest
from .types.apihub_service import DeleteApiRequest
from .types.apihub_service import DeleteAttributeRequest
from .types.apihub_service import DeleteDependencyRequest
from .types.apihub_service import DeleteDeploymentRequest
from .types.apihub_service import DeleteExternalApiRequest
from .types.apihub_service import DeleteSpecRequest
from .types.apihub_service import DeleteVersionRequest
from .types.apihub_service import GetApiOperationRequest
from .types.apihub_service import GetApiRequest
from .types.apihub_service import GetAttributeRequest
from .types.apihub_service import GetDefinitionRequest
from .types.apihub_service import GetDependencyRequest
from .types.apihub_service import GetDeploymentRequest
from .types.apihub_service import GetExternalApiRequest
from .types.apihub_service import GetSpecContentsRequest
from .types.apihub_service import GetSpecRequest
from .types.apihub_service import GetVersionRequest
from .types.apihub_service import ListApiOperationsRequest
from .types.apihub_service import ListApiOperationsResponse
from .types.apihub_service import ListApisRequest
from .types.apihub_service import ListApisResponse
from .types.apihub_service import ListAttributesRequest
from .types.apihub_service import ListAttributesResponse
from .types.apihub_service import ListDependenciesRequest
from .types.apihub_service import ListDependenciesResponse
from .types.apihub_service import ListDeploymentsRequest
from .types.apihub_service import ListDeploymentsResponse
from .types.apihub_service import ListExternalApisRequest
from .types.apihub_service import ListExternalApisResponse
from .types.apihub_service import ListSpecsRequest
from .types.apihub_service import ListSpecsResponse
from .types.apihub_service import ListVersionsRequest
from .types.apihub_service import ListVersionsResponse
from .types.apihub_service import SearchResourcesRequest
from .types.apihub_service import SearchResourcesResponse
from .types.apihub_service import SearchResult
from .types.apihub_service import UpdateApiRequest
from .types.apihub_service import UpdateAttributeRequest
from .types.apihub_service import UpdateDependencyRequest
from .types.apihub_service import UpdateDeploymentRequest
from .types.apihub_service import UpdateExternalApiRequest
from .types.apihub_service import UpdateSpecRequest
from .types.apihub_service import UpdateVersionRequest
from .types.common_fields import Api
from .types.common_fields import ApiHubInstance
from .types.common_fields import ApiOperation
from .types.common_fields import Attribute
from .types.common_fields import AttributeValues
from .types.common_fields import Definition
from .types.common_fields import Dependency
from .types.common_fields import DependencyEntityReference
from .types.common_fields import DependencyErrorDetail
from .types.common_fields import Deployment
from .types.common_fields import Documentation
from .types.common_fields import ExternalApi
from .types.common_fields import HttpOperation
from .types.common_fields import Issue
from .types.common_fields import LintResponse
from .types.common_fields import OpenApiSpecDetails
from .types.common_fields import OperationDetails
from .types.common_fields import OperationMetadata
from .types.common_fields import Owner
from .types.common_fields import Path
from .types.common_fields import Point
from .types.common_fields import Range
from .types.common_fields import Schema
from .types.common_fields import Spec
from .types.common_fields import SpecContents
from .types.common_fields import SpecDetails
from .types.common_fields import Version
from .types.common_fields import Linter
from .types.common_fields import LintState
from .types.common_fields import Severity
from .types.host_project_registration_service import CreateHostProjectRegistrationRequest
from .types.host_project_registration_service import GetHostProjectRegistrationRequest
from .types.host_project_registration_service import HostProjectRegistration
from .types.host_project_registration_service import ListHostProjectRegistrationsRequest
from .types.host_project_registration_service import ListHostProjectRegistrationsResponse
from .types.linting_service import GetStyleGuideContentsRequest
from .types.linting_service import GetStyleGuideRequest
from .types.linting_service import LintSpecRequest
from .types.linting_service import StyleGuide
from .types.linting_service import StyleGuideContents
from .types.linting_service import UpdateStyleGuideRequest
from .types.plugin_service import DisablePluginRequest
from .types.plugin_service import EnablePluginRequest
from .types.plugin_service import GetPluginRequest
from .types.plugin_service import Plugin
from .types.provisioning_service import CreateApiHubInstanceRequest
from .types.provisioning_service import GetApiHubInstanceRequest
from .types.provisioning_service import LookupApiHubInstanceRequest
from .types.provisioning_service import LookupApiHubInstanceResponse
from .types.runtime_project_attachment_service import CreateRuntimeProjectAttachmentRequest
from .types.runtime_project_attachment_service import DeleteRuntimeProjectAttachmentRequest
from .types.runtime_project_attachment_service import GetRuntimeProjectAttachmentRequest
from .types.runtime_project_attachment_service import ListRuntimeProjectAttachmentsRequest
from .types.runtime_project_attachment_service import ListRuntimeProjectAttachmentsResponse
from .types.runtime_project_attachment_service import LookupRuntimeProjectAttachmentRequest
from .types.runtime_project_attachment_service import LookupRuntimeProjectAttachmentResponse
from .types.runtime_project_attachment_service import RuntimeProjectAttachment

__all__ = (
    'ApiHubAsyncClient',
    'ApiHubDependenciesAsyncClient',
    'ApiHubPluginAsyncClient',
    'HostProjectRegistrationServiceAsyncClient',
    'LintingServiceAsyncClient',
    'ProvisioningAsyncClient',
    'RuntimeProjectAttachmentServiceAsyncClient',
'Api',
'ApiHubClient',
'ApiHubDependenciesClient',
'ApiHubInstance',
'ApiHubPluginClient',
'ApiHubResource',
'ApiOperation',
'Attribute',
'AttributeValues',
'CreateApiHubInstanceRequest',
'CreateApiRequest',
'CreateAttributeRequest',
'CreateDependencyRequest',
'CreateDeploymentRequest',
'CreateExternalApiRequest',
'CreateHostProjectRegistrationRequest',
'CreateRuntimeProjectAttachmentRequest',
'CreateSpecRequest',
'CreateVersionRequest',
'Definition',
'DeleteApiRequest',
'DeleteAttributeRequest',
'DeleteDependencyRequest',
'DeleteDeploymentRequest',
'DeleteExternalApiRequest',
'DeleteRuntimeProjectAttachmentRequest',
'DeleteSpecRequest',
'DeleteVersionRequest',
'Dependency',
'DependencyEntityReference',
'DependencyErrorDetail',
'Deployment',
'DisablePluginRequest',
'Documentation',
'EnablePluginRequest',
'ExternalApi',
'GetApiHubInstanceRequest',
'GetApiOperationRequest',
'GetApiRequest',
'GetAttributeRequest',
'GetDefinitionRequest',
'GetDependencyRequest',
'GetDeploymentRequest',
'GetExternalApiRequest',
'GetHostProjectRegistrationRequest',
'GetPluginRequest',
'GetRuntimeProjectAttachmentRequest',
'GetSpecContentsRequest',
'GetSpecRequest',
'GetStyleGuideContentsRequest',
'GetStyleGuideRequest',
'GetVersionRequest',
'HostProjectRegistration',
'HostProjectRegistrationServiceClient',
'HttpOperation',
'Issue',
'LintResponse',
'LintSpecRequest',
'LintState',
'Linter',
'LintingServiceClient',
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
'ListHostProjectRegistrationsRequest',
'ListHostProjectRegistrationsResponse',
'ListRuntimeProjectAttachmentsRequest',
'ListRuntimeProjectAttachmentsResponse',
'ListSpecsRequest',
'ListSpecsResponse',
'ListVersionsRequest',
'ListVersionsResponse',
'LookupApiHubInstanceRequest',
'LookupApiHubInstanceResponse',
'LookupRuntimeProjectAttachmentRequest',
'LookupRuntimeProjectAttachmentResponse',
'OpenApiSpecDetails',
'OperationDetails',
'OperationMetadata',
'Owner',
'Path',
'Plugin',
'Point',
'ProvisioningClient',
'Range',
'RuntimeProjectAttachment',
'RuntimeProjectAttachmentServiceClient',
'Schema',
'SearchResourcesRequest',
'SearchResourcesResponse',
'SearchResult',
'Severity',
'Spec',
'SpecContents',
'SpecDetails',
'StyleGuide',
'StyleGuideContents',
'UpdateApiRequest',
'UpdateAttributeRequest',
'UpdateDependencyRequest',
'UpdateDeploymentRequest',
'UpdateExternalApiRequest',
'UpdateSpecRequest',
'UpdateStyleGuideRequest',
'UpdateVersionRequest',
'Version',
)
