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
import sys

import google.api_core as api_core

from google.cloud.apihub_v1 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.api_hub import ApiHubAsyncClient, ApiHubClient
from .services.api_hub_collect import ApiHubCollectAsyncClient, ApiHubCollectClient
from .services.api_hub_curate import ApiHubCurateAsyncClient, ApiHubCurateClient
from .services.api_hub_dependencies import (
    ApiHubDependenciesAsyncClient,
    ApiHubDependenciesClient,
)
from .services.api_hub_discovery import (
    ApiHubDiscoveryAsyncClient,
    ApiHubDiscoveryClient,
)
from .services.api_hub_plugin import ApiHubPluginAsyncClient, ApiHubPluginClient
from .services.host_project_registration_service import (
    HostProjectRegistrationServiceAsyncClient,
    HostProjectRegistrationServiceClient,
)
from .services.linting_service import LintingServiceAsyncClient, LintingServiceClient
from .services.provisioning import ProvisioningAsyncClient, ProvisioningClient
from .services.runtime_project_attachment_service import (
    RuntimeProjectAttachmentServiceAsyncClient,
    RuntimeProjectAttachmentServiceClient,
)
from .types.apihub_service import (
    ApiHubResource,
    CreateApiOperationRequest,
    CreateApiRequest,
    CreateAttributeRequest,
    CreateDependencyRequest,
    CreateDeploymentRequest,
    CreateExternalApiRequest,
    CreateSpecRequest,
    CreateVersionRequest,
    DeleteApiOperationRequest,
    DeleteApiRequest,
    DeleteAttributeRequest,
    DeleteDependencyRequest,
    DeleteDeploymentRequest,
    DeleteExternalApiRequest,
    DeleteSpecRequest,
    DeleteVersionRequest,
    GetApiOperationRequest,
    GetApiRequest,
    GetAttributeRequest,
    GetDefinitionRequest,
    GetDependencyRequest,
    GetDeploymentRequest,
    GetExternalApiRequest,
    GetSpecContentsRequest,
    GetSpecRequest,
    GetVersionRequest,
    ListApiOperationsRequest,
    ListApiOperationsResponse,
    ListApisRequest,
    ListApisResponse,
    ListAttributesRequest,
    ListAttributesResponse,
    ListDependenciesRequest,
    ListDependenciesResponse,
    ListDeploymentsRequest,
    ListDeploymentsResponse,
    ListExternalApisRequest,
    ListExternalApisResponse,
    ListSpecsRequest,
    ListSpecsResponse,
    ListVersionsRequest,
    ListVersionsResponse,
    SearchResourcesRequest,
    SearchResourcesResponse,
    SearchResult,
    UpdateApiOperationRequest,
    UpdateApiRequest,
    UpdateAttributeRequest,
    UpdateDependencyRequest,
    UpdateDeploymentRequest,
    UpdateExternalApiRequest,
    UpdateSpecRequest,
    UpdateVersionRequest,
)
from .types.collect_service import (
    ApiData,
    APIMetadata,
    ApiMetadataList,
    CollectApiDataRequest,
    CollectApiDataResponse,
    CollectionType,
    DeploymentMetadata,
    SpecMetadata,
    VersionMetadata,
)
from .types.common_fields import (
    Api,
    ApiHubInstance,
    ApiOperation,
    Attribute,
    AttributeValues,
    AuthConfig,
    AuthType,
    ConfigValueOption,
    ConfigVariable,
    ConfigVariableTemplate,
    Definition,
    Dependency,
    DependencyEntityReference,
    DependencyErrorDetail,
    Deployment,
    DiscoveredApiObservation,
    DiscoveredApiOperation,
    Documentation,
    ExternalApi,
    GoogleServiceAccountConfig,
    HttpOperation,
    HttpOperationDetails,
    Issue,
    Linter,
    LintResponse,
    LintState,
    OpenApiSpecDetails,
    OperationDetails,
    OperationMetadata,
    Owner,
    Path,
    PluginCategory,
    Point,
    Range,
    Schema,
    Secret,
    Severity,
    SourceMetadata,
    Spec,
    SpecContents,
    SpecDetails,
    Version,
)
from .types.curate_service import (
    ApplicationIntegrationEndpointDetails,
    CreateCurationRequest,
    Curation,
    DeleteCurationRequest,
    Endpoint,
    GetCurationRequest,
    ListCurationsRequest,
    ListCurationsResponse,
    UpdateCurationRequest,
)
from .types.discovery_service import (
    GetDiscoveredApiObservationRequest,
    GetDiscoveredApiOperationRequest,
    ListDiscoveredApiObservationsRequest,
    ListDiscoveredApiObservationsResponse,
    ListDiscoveredApiOperationsRequest,
    ListDiscoveredApiOperationsResponse,
)
from .types.host_project_registration_service import (
    CreateHostProjectRegistrationRequest,
    GetHostProjectRegistrationRequest,
    HostProjectRegistration,
    ListHostProjectRegistrationsRequest,
    ListHostProjectRegistrationsResponse,
)
from .types.linting_service import (
    GetStyleGuideContentsRequest,
    GetStyleGuideRequest,
    LintSpecRequest,
    StyleGuide,
    StyleGuideContents,
    UpdateStyleGuideRequest,
)
from .types.plugin_service import (
    ActionExecutionDetail,
    ActionType,
    CreatePluginInstanceRequest,
    CreatePluginRequest,
    CurationConfig,
    CurationType,
    DeletePluginInstanceRequest,
    DeletePluginRequest,
    DisablePluginInstanceActionRequest,
    DisablePluginInstanceActionResponse,
    DisablePluginRequest,
    EnablePluginInstanceActionRequest,
    EnablePluginInstanceActionResponse,
    EnablePluginRequest,
    ExecutePluginInstanceActionRequest,
    ExecutePluginInstanceActionResponse,
    ExecutionStatus,
    GatewayType,
    GetPluginInstanceRequest,
    GetPluginRequest,
    ListPluginInstancesRequest,
    ListPluginInstancesResponse,
    ListPluginsRequest,
    ListPluginsResponse,
    Plugin,
    PluginActionConfig,
    PluginInstance,
    PluginInstanceAction,
    UpdatePluginInstanceRequest,
)
from .types.provisioning_service import (
    CreateApiHubInstanceRequest,
    DeleteApiHubInstanceRequest,
    GetApiHubInstanceRequest,
    LookupApiHubInstanceRequest,
    LookupApiHubInstanceResponse,
)
from .types.runtime_project_attachment_service import (
    CreateRuntimeProjectAttachmentRequest,
    DeleteRuntimeProjectAttachmentRequest,
    GetRuntimeProjectAttachmentRequest,
    ListRuntimeProjectAttachmentsRequest,
    ListRuntimeProjectAttachmentsResponse,
    LookupRuntimeProjectAttachmentRequest,
    LookupRuntimeProjectAttachmentResponse,
    RuntimeProjectAttachment,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.apihub_v1")  # type: ignore
    api_core.check_dependency_versions("google.cloud.apihub_v1")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.apihub_v1"
        if sys.version_info < (3, 9):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.9, and then update {_package_label}.",
                FutureWarning,
            )
        if sys.version_info[:2] == (3, 9):
            warnings.warn(
                f"You are using a Python version ({_py_version_str}) "
                + f"which Google will stop supporting in {_package_label} in "
                + "January 2026. Please "
                + "upgrade to the latest Python version, or at "
                + "least to Python 3.10, before then, and "
                + f"then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "4.25.8" -> (4, 25, 8)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(
                f"Package {_package_label} depends on "
                + f"{_dependency_package}, currently installed at version "
                + f"{_version_used_string}. Future updates to "
                + f"{_package_label} will require {_dependency_package} at "
                + f"version {_next_supported_version} or higher{_recommendation}."
                + " Please ensure "
                + "that either (a) your Python environment doesn't pin the "
                + f"version of {_dependency_package}, so that updates to "
                + f"{_package_label} can require the higher version, or "
                + "(b) you manually update your Python environment to use at "
                + f"least version {_next_supported_version} of "
                + f"{_dependency_package}.",
                FutureWarning,
            )
    except Exception:
        warnings.warn(
            "Could not determine the version of Python "
            + "currently being used. To continue receiving "
            + "updates for {_package_label}, ensure you are "
            + "using a supported version of Python; see "
            + "https://devguide.python.org/versions/"
        )

__all__ = (
    "ApiHubAsyncClient",
    "ApiHubCollectAsyncClient",
    "ApiHubCurateAsyncClient",
    "ApiHubDependenciesAsyncClient",
    "ApiHubDiscoveryAsyncClient",
    "ApiHubPluginAsyncClient",
    "HostProjectRegistrationServiceAsyncClient",
    "LintingServiceAsyncClient",
    "ProvisioningAsyncClient",
    "RuntimeProjectAttachmentServiceAsyncClient",
    "APIMetadata",
    "ActionExecutionDetail",
    "ActionType",
    "Api",
    "ApiData",
    "ApiHubClient",
    "ApiHubCollectClient",
    "ApiHubCurateClient",
    "ApiHubDependenciesClient",
    "ApiHubDiscoveryClient",
    "ApiHubInstance",
    "ApiHubPluginClient",
    "ApiHubResource",
    "ApiMetadataList",
    "ApiOperation",
    "ApplicationIntegrationEndpointDetails",
    "Attribute",
    "AttributeValues",
    "AuthConfig",
    "AuthType",
    "CollectApiDataRequest",
    "CollectApiDataResponse",
    "CollectionType",
    "ConfigValueOption",
    "ConfigVariable",
    "ConfigVariableTemplate",
    "CreateApiHubInstanceRequest",
    "CreateApiOperationRequest",
    "CreateApiRequest",
    "CreateAttributeRequest",
    "CreateCurationRequest",
    "CreateDependencyRequest",
    "CreateDeploymentRequest",
    "CreateExternalApiRequest",
    "CreateHostProjectRegistrationRequest",
    "CreatePluginInstanceRequest",
    "CreatePluginRequest",
    "CreateRuntimeProjectAttachmentRequest",
    "CreateSpecRequest",
    "CreateVersionRequest",
    "Curation",
    "CurationConfig",
    "CurationType",
    "Definition",
    "DeleteApiHubInstanceRequest",
    "DeleteApiOperationRequest",
    "DeleteApiRequest",
    "DeleteAttributeRequest",
    "DeleteCurationRequest",
    "DeleteDependencyRequest",
    "DeleteDeploymentRequest",
    "DeleteExternalApiRequest",
    "DeletePluginInstanceRequest",
    "DeletePluginRequest",
    "DeleteRuntimeProjectAttachmentRequest",
    "DeleteSpecRequest",
    "DeleteVersionRequest",
    "Dependency",
    "DependencyEntityReference",
    "DependencyErrorDetail",
    "Deployment",
    "DeploymentMetadata",
    "DisablePluginInstanceActionRequest",
    "DisablePluginInstanceActionResponse",
    "DisablePluginRequest",
    "DiscoveredApiObservation",
    "DiscoveredApiOperation",
    "Documentation",
    "EnablePluginInstanceActionRequest",
    "EnablePluginInstanceActionResponse",
    "EnablePluginRequest",
    "Endpoint",
    "ExecutePluginInstanceActionRequest",
    "ExecutePluginInstanceActionResponse",
    "ExecutionStatus",
    "ExternalApi",
    "GatewayType",
    "GetApiHubInstanceRequest",
    "GetApiOperationRequest",
    "GetApiRequest",
    "GetAttributeRequest",
    "GetCurationRequest",
    "GetDefinitionRequest",
    "GetDependencyRequest",
    "GetDeploymentRequest",
    "GetDiscoveredApiObservationRequest",
    "GetDiscoveredApiOperationRequest",
    "GetExternalApiRequest",
    "GetHostProjectRegistrationRequest",
    "GetPluginInstanceRequest",
    "GetPluginRequest",
    "GetRuntimeProjectAttachmentRequest",
    "GetSpecContentsRequest",
    "GetSpecRequest",
    "GetStyleGuideContentsRequest",
    "GetStyleGuideRequest",
    "GetVersionRequest",
    "GoogleServiceAccountConfig",
    "HostProjectRegistration",
    "HostProjectRegistrationServiceClient",
    "HttpOperation",
    "HttpOperationDetails",
    "Issue",
    "LintResponse",
    "LintSpecRequest",
    "LintState",
    "Linter",
    "LintingServiceClient",
    "ListApiOperationsRequest",
    "ListApiOperationsResponse",
    "ListApisRequest",
    "ListApisResponse",
    "ListAttributesRequest",
    "ListAttributesResponse",
    "ListCurationsRequest",
    "ListCurationsResponse",
    "ListDependenciesRequest",
    "ListDependenciesResponse",
    "ListDeploymentsRequest",
    "ListDeploymentsResponse",
    "ListDiscoveredApiObservationsRequest",
    "ListDiscoveredApiObservationsResponse",
    "ListDiscoveredApiOperationsRequest",
    "ListDiscoveredApiOperationsResponse",
    "ListExternalApisRequest",
    "ListExternalApisResponse",
    "ListHostProjectRegistrationsRequest",
    "ListHostProjectRegistrationsResponse",
    "ListPluginInstancesRequest",
    "ListPluginInstancesResponse",
    "ListPluginsRequest",
    "ListPluginsResponse",
    "ListRuntimeProjectAttachmentsRequest",
    "ListRuntimeProjectAttachmentsResponse",
    "ListSpecsRequest",
    "ListSpecsResponse",
    "ListVersionsRequest",
    "ListVersionsResponse",
    "LookupApiHubInstanceRequest",
    "LookupApiHubInstanceResponse",
    "LookupRuntimeProjectAttachmentRequest",
    "LookupRuntimeProjectAttachmentResponse",
    "OpenApiSpecDetails",
    "OperationDetails",
    "OperationMetadata",
    "Owner",
    "Path",
    "Plugin",
    "PluginActionConfig",
    "PluginCategory",
    "PluginInstance",
    "PluginInstanceAction",
    "Point",
    "ProvisioningClient",
    "Range",
    "RuntimeProjectAttachment",
    "RuntimeProjectAttachmentServiceClient",
    "Schema",
    "SearchResourcesRequest",
    "SearchResourcesResponse",
    "SearchResult",
    "Secret",
    "Severity",
    "SourceMetadata",
    "Spec",
    "SpecContents",
    "SpecDetails",
    "SpecMetadata",
    "StyleGuide",
    "StyleGuideContents",
    "UpdateApiOperationRequest",
    "UpdateApiRequest",
    "UpdateAttributeRequest",
    "UpdateCurationRequest",
    "UpdateDependencyRequest",
    "UpdateDeploymentRequest",
    "UpdateExternalApiRequest",
    "UpdatePluginInstanceRequest",
    "UpdateSpecRequest",
    "UpdateStyleGuideRequest",
    "UpdateVersionRequest",
    "Version",
    "VersionMetadata",
)
