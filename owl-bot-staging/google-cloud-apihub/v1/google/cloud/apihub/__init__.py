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
from google.cloud.apihub import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.apihub_v1.services.api_hub.client import ApiHubClient
from google.cloud.apihub_v1.services.api_hub.async_client import ApiHubAsyncClient
from google.cloud.apihub_v1.services.api_hub_collect.client import ApiHubCollectClient
from google.cloud.apihub_v1.services.api_hub_collect.async_client import ApiHubCollectAsyncClient
from google.cloud.apihub_v1.services.api_hub_curate.client import ApiHubCurateClient
from google.cloud.apihub_v1.services.api_hub_curate.async_client import ApiHubCurateAsyncClient
from google.cloud.apihub_v1.services.api_hub_dependencies.client import ApiHubDependenciesClient
from google.cloud.apihub_v1.services.api_hub_dependencies.async_client import ApiHubDependenciesAsyncClient
from google.cloud.apihub_v1.services.api_hub_discovery.client import ApiHubDiscoveryClient
from google.cloud.apihub_v1.services.api_hub_discovery.async_client import ApiHubDiscoveryAsyncClient
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
from google.cloud.apihub_v1.types.apihub_service import CreateApiOperationRequest
from google.cloud.apihub_v1.types.apihub_service import CreateApiRequest
from google.cloud.apihub_v1.types.apihub_service import CreateAttributeRequest
from google.cloud.apihub_v1.types.apihub_service import CreateDependencyRequest
from google.cloud.apihub_v1.types.apihub_service import CreateDeploymentRequest
from google.cloud.apihub_v1.types.apihub_service import CreateExternalApiRequest
from google.cloud.apihub_v1.types.apihub_service import CreateSpecRequest
from google.cloud.apihub_v1.types.apihub_service import CreateVersionRequest
from google.cloud.apihub_v1.types.apihub_service import DeleteApiOperationRequest
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
from google.cloud.apihub_v1.types.apihub_service import UpdateApiOperationRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateApiRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateAttributeRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateDependencyRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateDeploymentRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateExternalApiRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateSpecRequest
from google.cloud.apihub_v1.types.apihub_service import UpdateVersionRequest
from google.cloud.apihub_v1.types.collect_service import ApiData
from google.cloud.apihub_v1.types.collect_service import APIMetadata
from google.cloud.apihub_v1.types.collect_service import ApiMetadataList
from google.cloud.apihub_v1.types.collect_service import CollectApiDataRequest
from google.cloud.apihub_v1.types.collect_service import CollectApiDataResponse
from google.cloud.apihub_v1.types.collect_service import DeploymentMetadata
from google.cloud.apihub_v1.types.collect_service import SpecMetadata
from google.cloud.apihub_v1.types.collect_service import VersionMetadata
from google.cloud.apihub_v1.types.collect_service import CollectionType
from google.cloud.apihub_v1.types.common_fields import Api
from google.cloud.apihub_v1.types.common_fields import ApiHubInstance
from google.cloud.apihub_v1.types.common_fields import ApiOperation
from google.cloud.apihub_v1.types.common_fields import Attribute
from google.cloud.apihub_v1.types.common_fields import AttributeValues
from google.cloud.apihub_v1.types.common_fields import AuthConfig
from google.cloud.apihub_v1.types.common_fields import ConfigValueOption
from google.cloud.apihub_v1.types.common_fields import ConfigVariable
from google.cloud.apihub_v1.types.common_fields import ConfigVariableTemplate
from google.cloud.apihub_v1.types.common_fields import Definition
from google.cloud.apihub_v1.types.common_fields import Dependency
from google.cloud.apihub_v1.types.common_fields import DependencyEntityReference
from google.cloud.apihub_v1.types.common_fields import DependencyErrorDetail
from google.cloud.apihub_v1.types.common_fields import Deployment
from google.cloud.apihub_v1.types.common_fields import DiscoveredApiObservation
from google.cloud.apihub_v1.types.common_fields import DiscoveredApiOperation
from google.cloud.apihub_v1.types.common_fields import Documentation
from google.cloud.apihub_v1.types.common_fields import ExternalApi
from google.cloud.apihub_v1.types.common_fields import GoogleServiceAccountConfig
from google.cloud.apihub_v1.types.common_fields import HttpOperation
from google.cloud.apihub_v1.types.common_fields import HttpOperationDetails
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
from google.cloud.apihub_v1.types.common_fields import Secret
from google.cloud.apihub_v1.types.common_fields import SourceMetadata
from google.cloud.apihub_v1.types.common_fields import Spec
from google.cloud.apihub_v1.types.common_fields import SpecContents
from google.cloud.apihub_v1.types.common_fields import SpecDetails
from google.cloud.apihub_v1.types.common_fields import Version
from google.cloud.apihub_v1.types.common_fields import AuthType
from google.cloud.apihub_v1.types.common_fields import Linter
from google.cloud.apihub_v1.types.common_fields import LintState
from google.cloud.apihub_v1.types.common_fields import PluginCategory
from google.cloud.apihub_v1.types.common_fields import Severity
from google.cloud.apihub_v1.types.curate_service import ApplicationIntegrationEndpointDetails
from google.cloud.apihub_v1.types.curate_service import CreateCurationRequest
from google.cloud.apihub_v1.types.curate_service import Curation
from google.cloud.apihub_v1.types.curate_service import DeleteCurationRequest
from google.cloud.apihub_v1.types.curate_service import Endpoint
from google.cloud.apihub_v1.types.curate_service import GetCurationRequest
from google.cloud.apihub_v1.types.curate_service import ListCurationsRequest
from google.cloud.apihub_v1.types.curate_service import ListCurationsResponse
from google.cloud.apihub_v1.types.curate_service import UpdateCurationRequest
from google.cloud.apihub_v1.types.discovery_service import GetDiscoveredApiObservationRequest
from google.cloud.apihub_v1.types.discovery_service import GetDiscoveredApiOperationRequest
from google.cloud.apihub_v1.types.discovery_service import ListDiscoveredApiObservationsRequest
from google.cloud.apihub_v1.types.discovery_service import ListDiscoveredApiObservationsResponse
from google.cloud.apihub_v1.types.discovery_service import ListDiscoveredApiOperationsRequest
from google.cloud.apihub_v1.types.discovery_service import ListDiscoveredApiOperationsResponse
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
from google.cloud.apihub_v1.types.plugin_service import ActionExecutionDetail
from google.cloud.apihub_v1.types.plugin_service import CreatePluginInstanceRequest
from google.cloud.apihub_v1.types.plugin_service import CreatePluginRequest
from google.cloud.apihub_v1.types.plugin_service import CurationConfig
from google.cloud.apihub_v1.types.plugin_service import DeletePluginInstanceRequest
from google.cloud.apihub_v1.types.plugin_service import DeletePluginRequest
from google.cloud.apihub_v1.types.plugin_service import DisablePluginInstanceActionRequest
from google.cloud.apihub_v1.types.plugin_service import DisablePluginInstanceActionResponse
from google.cloud.apihub_v1.types.plugin_service import DisablePluginRequest
from google.cloud.apihub_v1.types.plugin_service import EnablePluginInstanceActionRequest
from google.cloud.apihub_v1.types.plugin_service import EnablePluginInstanceActionResponse
from google.cloud.apihub_v1.types.plugin_service import EnablePluginRequest
from google.cloud.apihub_v1.types.plugin_service import ExecutePluginInstanceActionRequest
from google.cloud.apihub_v1.types.plugin_service import ExecutePluginInstanceActionResponse
from google.cloud.apihub_v1.types.plugin_service import ExecutionStatus
from google.cloud.apihub_v1.types.plugin_service import GetPluginInstanceRequest
from google.cloud.apihub_v1.types.plugin_service import GetPluginRequest
from google.cloud.apihub_v1.types.plugin_service import ListPluginInstancesRequest
from google.cloud.apihub_v1.types.plugin_service import ListPluginInstancesResponse
from google.cloud.apihub_v1.types.plugin_service import ListPluginsRequest
from google.cloud.apihub_v1.types.plugin_service import ListPluginsResponse
from google.cloud.apihub_v1.types.plugin_service import Plugin
from google.cloud.apihub_v1.types.plugin_service import PluginActionConfig
from google.cloud.apihub_v1.types.plugin_service import PluginInstance
from google.cloud.apihub_v1.types.plugin_service import PluginInstanceAction
from google.cloud.apihub_v1.types.plugin_service import UpdatePluginInstanceRequest
from google.cloud.apihub_v1.types.plugin_service import ActionType
from google.cloud.apihub_v1.types.plugin_service import CurationType
from google.cloud.apihub_v1.types.plugin_service import GatewayType
from google.cloud.apihub_v1.types.provisioning_service import CreateApiHubInstanceRequest
from google.cloud.apihub_v1.types.provisioning_service import DeleteApiHubInstanceRequest
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
    'ApiHubCollectClient',
    'ApiHubCollectAsyncClient',
    'ApiHubCurateClient',
    'ApiHubCurateAsyncClient',
    'ApiHubDependenciesClient',
    'ApiHubDependenciesAsyncClient',
    'ApiHubDiscoveryClient',
    'ApiHubDiscoveryAsyncClient',
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
    'CreateApiOperationRequest',
    'CreateApiRequest',
    'CreateAttributeRequest',
    'CreateDependencyRequest',
    'CreateDeploymentRequest',
    'CreateExternalApiRequest',
    'CreateSpecRequest',
    'CreateVersionRequest',
    'DeleteApiOperationRequest',
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
    'UpdateApiOperationRequest',
    'UpdateApiRequest',
    'UpdateAttributeRequest',
    'UpdateDependencyRequest',
    'UpdateDeploymentRequest',
    'UpdateExternalApiRequest',
    'UpdateSpecRequest',
    'UpdateVersionRequest',
    'ApiData',
    'APIMetadata',
    'ApiMetadataList',
    'CollectApiDataRequest',
    'CollectApiDataResponse',
    'DeploymentMetadata',
    'SpecMetadata',
    'VersionMetadata',
    'CollectionType',
    'Api',
    'ApiHubInstance',
    'ApiOperation',
    'Attribute',
    'AttributeValues',
    'AuthConfig',
    'ConfigValueOption',
    'ConfigVariable',
    'ConfigVariableTemplate',
    'Definition',
    'Dependency',
    'DependencyEntityReference',
    'DependencyErrorDetail',
    'Deployment',
    'DiscoveredApiObservation',
    'DiscoveredApiOperation',
    'Documentation',
    'ExternalApi',
    'GoogleServiceAccountConfig',
    'HttpOperation',
    'HttpOperationDetails',
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
    'Secret',
    'SourceMetadata',
    'Spec',
    'SpecContents',
    'SpecDetails',
    'Version',
    'AuthType',
    'Linter',
    'LintState',
    'PluginCategory',
    'Severity',
    'ApplicationIntegrationEndpointDetails',
    'CreateCurationRequest',
    'Curation',
    'DeleteCurationRequest',
    'Endpoint',
    'GetCurationRequest',
    'ListCurationsRequest',
    'ListCurationsResponse',
    'UpdateCurationRequest',
    'GetDiscoveredApiObservationRequest',
    'GetDiscoveredApiOperationRequest',
    'ListDiscoveredApiObservationsRequest',
    'ListDiscoveredApiObservationsResponse',
    'ListDiscoveredApiOperationsRequest',
    'ListDiscoveredApiOperationsResponse',
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
    'ActionExecutionDetail',
    'CreatePluginInstanceRequest',
    'CreatePluginRequest',
    'CurationConfig',
    'DeletePluginInstanceRequest',
    'DeletePluginRequest',
    'DisablePluginInstanceActionRequest',
    'DisablePluginInstanceActionResponse',
    'DisablePluginRequest',
    'EnablePluginInstanceActionRequest',
    'EnablePluginInstanceActionResponse',
    'EnablePluginRequest',
    'ExecutePluginInstanceActionRequest',
    'ExecutePluginInstanceActionResponse',
    'ExecutionStatus',
    'GetPluginInstanceRequest',
    'GetPluginRequest',
    'ListPluginInstancesRequest',
    'ListPluginInstancesResponse',
    'ListPluginsRequest',
    'ListPluginsResponse',
    'Plugin',
    'PluginActionConfig',
    'PluginInstance',
    'PluginInstanceAction',
    'UpdatePluginInstanceRequest',
    'ActionType',
    'CurationType',
    'GatewayType',
    'CreateApiHubInstanceRequest',
    'DeleteApiHubInstanceRequest',
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
