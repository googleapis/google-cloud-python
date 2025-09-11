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
from google.cloud.apihub_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.api_hub import ApiHubClient
from .services.api_hub_collect import ApiHubCollectClient
from .services.api_hub_curate import ApiHubCurateClient
from .services.api_hub_dependencies import ApiHubDependenciesClient
from .services.api_hub_discovery import ApiHubDiscoveryClient
from .services.api_hub_plugin import ApiHubPluginClient
from .services.host_project_registration_service import HostProjectRegistrationServiceClient
from .services.linting_service import LintingServiceClient
from .services.provisioning import ProvisioningClient
from .services.runtime_project_attachment_service import RuntimeProjectAttachmentServiceClient

from .types.apihub_service import ApiHubResource
from .types.apihub_service import CreateApiOperationRequest
from .types.apihub_service import CreateApiRequest
from .types.apihub_service import CreateAttributeRequest
from .types.apihub_service import CreateDependencyRequest
from .types.apihub_service import CreateDeploymentRequest
from .types.apihub_service import CreateExternalApiRequest
from .types.apihub_service import CreateSpecRequest
from .types.apihub_service import CreateVersionRequest
from .types.apihub_service import DeleteApiOperationRequest
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
from .types.apihub_service import UpdateApiOperationRequest
from .types.apihub_service import UpdateApiRequest
from .types.apihub_service import UpdateAttributeRequest
from .types.apihub_service import UpdateDependencyRequest
from .types.apihub_service import UpdateDeploymentRequest
from .types.apihub_service import UpdateExternalApiRequest
from .types.apihub_service import UpdateSpecRequest
from .types.apihub_service import UpdateVersionRequest
from .types.collect_service import ApiData
from .types.collect_service import APIMetadata
from .types.collect_service import ApiMetadataList
from .types.collect_service import CollectApiDataRequest
from .types.collect_service import CollectApiDataResponse
from .types.collect_service import DeploymentMetadata
from .types.collect_service import SpecMetadata
from .types.collect_service import VersionMetadata
from .types.collect_service import CollectionType
from .types.common_fields import Api
from .types.common_fields import ApiHubInstance
from .types.common_fields import ApiOperation
from .types.common_fields import Attribute
from .types.common_fields import AttributeValues
from .types.common_fields import AuthConfig
from .types.common_fields import ConfigValueOption
from .types.common_fields import ConfigVariable
from .types.common_fields import ConfigVariableTemplate
from .types.common_fields import Definition
from .types.common_fields import Dependency
from .types.common_fields import DependencyEntityReference
from .types.common_fields import DependencyErrorDetail
from .types.common_fields import Deployment
from .types.common_fields import DiscoveredApiObservation
from .types.common_fields import DiscoveredApiOperation
from .types.common_fields import Documentation
from .types.common_fields import ExternalApi
from .types.common_fields import GoogleServiceAccountConfig
from .types.common_fields import HttpOperation
from .types.common_fields import HttpOperationDetails
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
from .types.common_fields import Secret
from .types.common_fields import SourceMetadata
from .types.common_fields import Spec
from .types.common_fields import SpecContents
from .types.common_fields import SpecDetails
from .types.common_fields import Version
from .types.common_fields import AuthType
from .types.common_fields import Linter
from .types.common_fields import LintState
from .types.common_fields import PluginCategory
from .types.common_fields import Severity
from .types.curate_service import ApplicationIntegrationEndpointDetails
from .types.curate_service import CreateCurationRequest
from .types.curate_service import Curation
from .types.curate_service import DeleteCurationRequest
from .types.curate_service import Endpoint
from .types.curate_service import GetCurationRequest
from .types.curate_service import ListCurationsRequest
from .types.curate_service import ListCurationsResponse
from .types.curate_service import UpdateCurationRequest
from .types.discovery_service import GetDiscoveredApiObservationRequest
from .types.discovery_service import GetDiscoveredApiOperationRequest
from .types.discovery_service import ListDiscoveredApiObservationsRequest
from .types.discovery_service import ListDiscoveredApiObservationsResponse
from .types.discovery_service import ListDiscoveredApiOperationsRequest
from .types.discovery_service import ListDiscoveredApiOperationsResponse
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
from .types.plugin_service import ActionExecutionDetail
from .types.plugin_service import CreatePluginInstanceRequest
from .types.plugin_service import CreatePluginRequest
from .types.plugin_service import CurationConfig
from .types.plugin_service import DeletePluginInstanceRequest
from .types.plugin_service import DeletePluginRequest
from .types.plugin_service import DisablePluginInstanceActionRequest
from .types.plugin_service import DisablePluginInstanceActionResponse
from .types.plugin_service import DisablePluginRequest
from .types.plugin_service import EnablePluginInstanceActionRequest
from .types.plugin_service import EnablePluginInstanceActionResponse
from .types.plugin_service import EnablePluginRequest
from .types.plugin_service import ExecutePluginInstanceActionRequest
from .types.plugin_service import ExecutePluginInstanceActionResponse
from .types.plugin_service import ExecutionStatus
from .types.plugin_service import GetPluginInstanceRequest
from .types.plugin_service import GetPluginRequest
from .types.plugin_service import ListPluginInstancesRequest
from .types.plugin_service import ListPluginInstancesResponse
from .types.plugin_service import ListPluginsRequest
from .types.plugin_service import ListPluginsResponse
from .types.plugin_service import Plugin
from .types.plugin_service import PluginActionConfig
from .types.plugin_service import PluginInstance
from .types.plugin_service import PluginInstanceAction
from .types.plugin_service import UpdatePluginInstanceRequest
from .types.plugin_service import ActionType
from .types.plugin_service import CurationType
from .types.plugin_service import GatewayType
from .types.provisioning_service import CreateApiHubInstanceRequest
from .types.provisioning_service import DeleteApiHubInstanceRequest
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
'APIMetadata',
'ActionExecutionDetail',
'ActionType',
'Api',
'ApiData',
'ApiHubClient',
'ApiHubCollectClient',
'ApiHubCurateClient',
'ApiHubDependenciesClient',
'ApiHubDiscoveryClient',
'ApiHubInstance',
'ApiHubPluginClient',
'ApiHubResource',
'ApiMetadataList',
'ApiOperation',
'ApplicationIntegrationEndpointDetails',
'Attribute',
'AttributeValues',
'AuthConfig',
'AuthType',
'CollectApiDataRequest',
'CollectApiDataResponse',
'CollectionType',
'ConfigValueOption',
'ConfigVariable',
'ConfigVariableTemplate',
'CreateApiHubInstanceRequest',
'CreateApiOperationRequest',
'CreateApiRequest',
'CreateAttributeRequest',
'CreateCurationRequest',
'CreateDependencyRequest',
'CreateDeploymentRequest',
'CreateExternalApiRequest',
'CreateHostProjectRegistrationRequest',
'CreatePluginInstanceRequest',
'CreatePluginRequest',
'CreateRuntimeProjectAttachmentRequest',
'CreateSpecRequest',
'CreateVersionRequest',
'Curation',
'CurationConfig',
'CurationType',
'Definition',
'DeleteApiHubInstanceRequest',
'DeleteApiOperationRequest',
'DeleteApiRequest',
'DeleteAttributeRequest',
'DeleteCurationRequest',
'DeleteDependencyRequest',
'DeleteDeploymentRequest',
'DeleteExternalApiRequest',
'DeletePluginInstanceRequest',
'DeletePluginRequest',
'DeleteRuntimeProjectAttachmentRequest',
'DeleteSpecRequest',
'DeleteVersionRequest',
'Dependency',
'DependencyEntityReference',
'DependencyErrorDetail',
'Deployment',
'DeploymentMetadata',
'DisablePluginInstanceActionRequest',
'DisablePluginInstanceActionResponse',
'DisablePluginRequest',
'DiscoveredApiObservation',
'DiscoveredApiOperation',
'Documentation',
'EnablePluginInstanceActionRequest',
'EnablePluginInstanceActionResponse',
'EnablePluginRequest',
'Endpoint',
'ExecutePluginInstanceActionRequest',
'ExecutePluginInstanceActionResponse',
'ExecutionStatus',
'ExternalApi',
'GatewayType',
'GetApiHubInstanceRequest',
'GetApiOperationRequest',
'GetApiRequest',
'GetAttributeRequest',
'GetCurationRequest',
'GetDefinitionRequest',
'GetDependencyRequest',
'GetDeploymentRequest',
'GetDiscoveredApiObservationRequest',
'GetDiscoveredApiOperationRequest',
'GetExternalApiRequest',
'GetHostProjectRegistrationRequest',
'GetPluginInstanceRequest',
'GetPluginRequest',
'GetRuntimeProjectAttachmentRequest',
'GetSpecContentsRequest',
'GetSpecRequest',
'GetStyleGuideContentsRequest',
'GetStyleGuideRequest',
'GetVersionRequest',
'GoogleServiceAccountConfig',
'HostProjectRegistration',
'HostProjectRegistrationServiceClient',
'HttpOperation',
'HttpOperationDetails',
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
'ListCurationsRequest',
'ListCurationsResponse',
'ListDependenciesRequest',
'ListDependenciesResponse',
'ListDeploymentsRequest',
'ListDeploymentsResponse',
'ListDiscoveredApiObservationsRequest',
'ListDiscoveredApiObservationsResponse',
'ListDiscoveredApiOperationsRequest',
'ListDiscoveredApiOperationsResponse',
'ListExternalApisRequest',
'ListExternalApisResponse',
'ListHostProjectRegistrationsRequest',
'ListHostProjectRegistrationsResponse',
'ListPluginInstancesRequest',
'ListPluginInstancesResponse',
'ListPluginsRequest',
'ListPluginsResponse',
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
'PluginActionConfig',
'PluginCategory',
'PluginInstance',
'PluginInstanceAction',
'Point',
'ProvisioningClient',
'Range',
'RuntimeProjectAttachment',
'RuntimeProjectAttachmentServiceClient',
'Schema',
'SearchResourcesRequest',
'SearchResourcesResponse',
'SearchResult',
'Secret',
'Severity',
'SourceMetadata',
'Spec',
'SpecContents',
'SpecDetails',
'SpecMetadata',
'StyleGuide',
'StyleGuideContents',
'UpdateApiOperationRequest',
'UpdateApiRequest',
'UpdateAttributeRequest',
'UpdateCurationRequest',
'UpdateDependencyRequest',
'UpdateDeploymentRequest',
'UpdateExternalApiRequest',
'UpdatePluginInstanceRequest',
'UpdateSpecRequest',
'UpdateStyleGuideRequest',
'UpdateVersionRequest',
'Version',
'VersionMetadata',
)
