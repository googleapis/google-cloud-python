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

from google.cloud.dataplex_v1 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.business_glossary_service import (
    BusinessGlossaryServiceAsyncClient,
    BusinessGlossaryServiceClient,
)
from .services.catalog_service import CatalogServiceAsyncClient, CatalogServiceClient
from .services.cmek_service import CmekServiceAsyncClient, CmekServiceClient
from .services.content_service import ContentServiceAsyncClient, ContentServiceClient
from .services.data_scan_service import (
    DataScanServiceAsyncClient,
    DataScanServiceClient,
)
from .services.data_taxonomy_service import (
    DataTaxonomyServiceAsyncClient,
    DataTaxonomyServiceClient,
)
from .services.dataplex_service import DataplexServiceAsyncClient, DataplexServiceClient
from .services.metadata_service import MetadataServiceAsyncClient, MetadataServiceClient
from .types.analyze import Content, Environment, Session
from .types.business_glossary import (
    CreateGlossaryCategoryRequest,
    CreateGlossaryRequest,
    CreateGlossaryTermRequest,
    DeleteGlossaryCategoryRequest,
    DeleteGlossaryRequest,
    DeleteGlossaryTermRequest,
    GetGlossaryCategoryRequest,
    GetGlossaryRequest,
    GetGlossaryTermRequest,
    Glossary,
    GlossaryCategory,
    GlossaryTerm,
    ListGlossariesRequest,
    ListGlossariesResponse,
    ListGlossaryCategoriesRequest,
    ListGlossaryCategoriesResponse,
    ListGlossaryTermsRequest,
    ListGlossaryTermsResponse,
    UpdateGlossaryCategoryRequest,
    UpdateGlossaryRequest,
    UpdateGlossaryTermRequest,
)
from .types.catalog import (
    Aspect,
    AspectSource,
    AspectType,
    CancelMetadataJobRequest,
    CreateAspectTypeRequest,
    CreateEntryGroupRequest,
    CreateEntryLinkRequest,
    CreateEntryRequest,
    CreateEntryTypeRequest,
    CreateMetadataJobRequest,
    DeleteAspectTypeRequest,
    DeleteEntryGroupRequest,
    DeleteEntryLinkRequest,
    DeleteEntryRequest,
    DeleteEntryTypeRequest,
    Entry,
    EntryGroup,
    EntryLink,
    EntrySource,
    EntryType,
    EntryView,
    GetAspectTypeRequest,
    GetEntryGroupRequest,
    GetEntryLinkRequest,
    GetEntryRequest,
    GetEntryTypeRequest,
    GetMetadataJobRequest,
    ImportItem,
    ListAspectTypesRequest,
    ListAspectTypesResponse,
    ListEntriesRequest,
    ListEntriesResponse,
    ListEntryGroupsRequest,
    ListEntryGroupsResponse,
    ListEntryTypesRequest,
    ListEntryTypesResponse,
    ListMetadataJobsRequest,
    ListMetadataJobsResponse,
    LookupEntryRequest,
    MetadataJob,
    SearchEntriesRequest,
    SearchEntriesResponse,
    SearchEntriesResult,
    TransferStatus,
    UpdateAspectTypeRequest,
    UpdateEntryGroupRequest,
    UpdateEntryRequest,
    UpdateEntryTypeRequest,
)
from .types.cmek import (
    CreateEncryptionConfigRequest,
    DeleteEncryptionConfigRequest,
    EncryptionConfig,
    GetEncryptionConfigRequest,
    ListEncryptionConfigsRequest,
    ListEncryptionConfigsResponse,
    UpdateEncryptionConfigRequest,
)
from .types.content import (
    CreateContentRequest,
    DeleteContentRequest,
    GetContentRequest,
    ListContentRequest,
    ListContentResponse,
    UpdateContentRequest,
)
from .types.data_discovery import DataDiscoveryResult, DataDiscoverySpec
from .types.data_documentation import DataDocumentationResult, DataDocumentationSpec
from .types.data_profile import DataProfileResult, DataProfileSpec
from .types.data_quality import (
    DataQualityColumnResult,
    DataQualityDimension,
    DataQualityDimensionResult,
    DataQualityResult,
    DataQualityRule,
    DataQualityRuleResult,
    DataQualitySpec,
)
from .types.data_taxonomy import (
    CreateDataAttributeBindingRequest,
    CreateDataAttributeRequest,
    CreateDataTaxonomyRequest,
    DataAttribute,
    DataAttributeBinding,
    DataTaxonomy,
    DeleteDataAttributeBindingRequest,
    DeleteDataAttributeRequest,
    DeleteDataTaxonomyRequest,
    GetDataAttributeBindingRequest,
    GetDataAttributeRequest,
    GetDataTaxonomyRequest,
    ListDataAttributeBindingsRequest,
    ListDataAttributeBindingsResponse,
    ListDataAttributesRequest,
    ListDataAttributesResponse,
    ListDataTaxonomiesRequest,
    ListDataTaxonomiesResponse,
    UpdateDataAttributeBindingRequest,
    UpdateDataAttributeRequest,
    UpdateDataTaxonomyRequest,
)
from .types.datascans import (
    CreateDataScanRequest,
    DataScan,
    DataScanJob,
    DataScanType,
    DeleteDataScanRequest,
    GenerateDataQualityRulesRequest,
    GenerateDataQualityRulesResponse,
    GetDataScanJobRequest,
    GetDataScanRequest,
    ListDataScanJobsRequest,
    ListDataScanJobsResponse,
    ListDataScansRequest,
    ListDataScansResponse,
    RunDataScanRequest,
    RunDataScanResponse,
    UpdateDataScanRequest,
)
from .types.datascans_common import DataScanCatalogPublishingStatus
from .types.logs import (
    BusinessGlossaryEvent,
    DataQualityScanRuleResult,
    DataScanEvent,
    DiscoveryEvent,
    EntryLinkEvent,
    GovernanceEvent,
    JobEvent,
    SessionEvent,
)
from .types.metadata_ import (
    CreateEntityRequest,
    CreatePartitionRequest,
    DeleteEntityRequest,
    DeletePartitionRequest,
    Entity,
    GetEntityRequest,
    GetPartitionRequest,
    ListEntitiesRequest,
    ListEntitiesResponse,
    ListPartitionsRequest,
    ListPartitionsResponse,
    Partition,
    Schema,
    StorageAccess,
    StorageFormat,
    StorageSystem,
    UpdateEntityRequest,
)
from .types.processing import DataSource, ScannedData, Trigger
from .types.resources import Action, Asset, AssetStatus, Lake, State, Zone
from .types.security import DataAccessSpec, ResourceAccessSpec
from .types.service import (
    CancelJobRequest,
    CreateAssetRequest,
    CreateEnvironmentRequest,
    CreateLakeRequest,
    CreateTaskRequest,
    CreateZoneRequest,
    DeleteAssetRequest,
    DeleteEnvironmentRequest,
    DeleteLakeRequest,
    DeleteTaskRequest,
    DeleteZoneRequest,
    GetAssetRequest,
    GetEnvironmentRequest,
    GetJobRequest,
    GetLakeRequest,
    GetTaskRequest,
    GetZoneRequest,
    ListActionsResponse,
    ListAssetActionsRequest,
    ListAssetsRequest,
    ListAssetsResponse,
    ListEnvironmentsRequest,
    ListEnvironmentsResponse,
    ListJobsRequest,
    ListJobsResponse,
    ListLakeActionsRequest,
    ListLakesRequest,
    ListLakesResponse,
    ListSessionsRequest,
    ListSessionsResponse,
    ListTasksRequest,
    ListTasksResponse,
    ListZoneActionsRequest,
    ListZonesRequest,
    ListZonesResponse,
    OperationMetadata,
    RunTaskRequest,
    RunTaskResponse,
    UpdateAssetRequest,
    UpdateEnvironmentRequest,
    UpdateLakeRequest,
    UpdateTaskRequest,
    UpdateZoneRequest,
)
from .types.tasks import Job, Task

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.dataplex_v1")  # type: ignore
    api_core.check_dependency_versions("google.cloud.dataplex_v1")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.dataplex_v1"
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
    "BusinessGlossaryServiceAsyncClient",
    "CatalogServiceAsyncClient",
    "CmekServiceAsyncClient",
    "ContentServiceAsyncClient",
    "DataScanServiceAsyncClient",
    "DataTaxonomyServiceAsyncClient",
    "DataplexServiceAsyncClient",
    "MetadataServiceAsyncClient",
    "Action",
    "Aspect",
    "AspectSource",
    "AspectType",
    "Asset",
    "AssetStatus",
    "BusinessGlossaryEvent",
    "BusinessGlossaryServiceClient",
    "CancelJobRequest",
    "CancelMetadataJobRequest",
    "CatalogServiceClient",
    "CmekServiceClient",
    "Content",
    "ContentServiceClient",
    "CreateAspectTypeRequest",
    "CreateAssetRequest",
    "CreateContentRequest",
    "CreateDataAttributeBindingRequest",
    "CreateDataAttributeRequest",
    "CreateDataScanRequest",
    "CreateDataTaxonomyRequest",
    "CreateEncryptionConfigRequest",
    "CreateEntityRequest",
    "CreateEntryGroupRequest",
    "CreateEntryLinkRequest",
    "CreateEntryRequest",
    "CreateEntryTypeRequest",
    "CreateEnvironmentRequest",
    "CreateGlossaryCategoryRequest",
    "CreateGlossaryRequest",
    "CreateGlossaryTermRequest",
    "CreateLakeRequest",
    "CreateMetadataJobRequest",
    "CreatePartitionRequest",
    "CreateTaskRequest",
    "CreateZoneRequest",
    "DataAccessSpec",
    "DataAttribute",
    "DataAttributeBinding",
    "DataDiscoveryResult",
    "DataDiscoverySpec",
    "DataDocumentationResult",
    "DataDocumentationSpec",
    "DataProfileResult",
    "DataProfileSpec",
    "DataQualityColumnResult",
    "DataQualityDimension",
    "DataQualityDimensionResult",
    "DataQualityResult",
    "DataQualityRule",
    "DataQualityRuleResult",
    "DataQualityScanRuleResult",
    "DataQualitySpec",
    "DataScan",
    "DataScanCatalogPublishingStatus",
    "DataScanEvent",
    "DataScanJob",
    "DataScanServiceClient",
    "DataScanType",
    "DataSource",
    "DataTaxonomy",
    "DataTaxonomyServiceClient",
    "DataplexServiceClient",
    "DeleteAspectTypeRequest",
    "DeleteAssetRequest",
    "DeleteContentRequest",
    "DeleteDataAttributeBindingRequest",
    "DeleteDataAttributeRequest",
    "DeleteDataScanRequest",
    "DeleteDataTaxonomyRequest",
    "DeleteEncryptionConfigRequest",
    "DeleteEntityRequest",
    "DeleteEntryGroupRequest",
    "DeleteEntryLinkRequest",
    "DeleteEntryRequest",
    "DeleteEntryTypeRequest",
    "DeleteEnvironmentRequest",
    "DeleteGlossaryCategoryRequest",
    "DeleteGlossaryRequest",
    "DeleteGlossaryTermRequest",
    "DeleteLakeRequest",
    "DeletePartitionRequest",
    "DeleteTaskRequest",
    "DeleteZoneRequest",
    "DiscoveryEvent",
    "EncryptionConfig",
    "Entity",
    "Entry",
    "EntryGroup",
    "EntryLink",
    "EntryLinkEvent",
    "EntrySource",
    "EntryType",
    "EntryView",
    "Environment",
    "GenerateDataQualityRulesRequest",
    "GenerateDataQualityRulesResponse",
    "GetAspectTypeRequest",
    "GetAssetRequest",
    "GetContentRequest",
    "GetDataAttributeBindingRequest",
    "GetDataAttributeRequest",
    "GetDataScanJobRequest",
    "GetDataScanRequest",
    "GetDataTaxonomyRequest",
    "GetEncryptionConfigRequest",
    "GetEntityRequest",
    "GetEntryGroupRequest",
    "GetEntryLinkRequest",
    "GetEntryRequest",
    "GetEntryTypeRequest",
    "GetEnvironmentRequest",
    "GetGlossaryCategoryRequest",
    "GetGlossaryRequest",
    "GetGlossaryTermRequest",
    "GetJobRequest",
    "GetLakeRequest",
    "GetMetadataJobRequest",
    "GetPartitionRequest",
    "GetTaskRequest",
    "GetZoneRequest",
    "Glossary",
    "GlossaryCategory",
    "GlossaryTerm",
    "GovernanceEvent",
    "ImportItem",
    "Job",
    "JobEvent",
    "Lake",
    "ListActionsResponse",
    "ListAspectTypesRequest",
    "ListAspectTypesResponse",
    "ListAssetActionsRequest",
    "ListAssetsRequest",
    "ListAssetsResponse",
    "ListContentRequest",
    "ListContentResponse",
    "ListDataAttributeBindingsRequest",
    "ListDataAttributeBindingsResponse",
    "ListDataAttributesRequest",
    "ListDataAttributesResponse",
    "ListDataScanJobsRequest",
    "ListDataScanJobsResponse",
    "ListDataScansRequest",
    "ListDataScansResponse",
    "ListDataTaxonomiesRequest",
    "ListDataTaxonomiesResponse",
    "ListEncryptionConfigsRequest",
    "ListEncryptionConfigsResponse",
    "ListEntitiesRequest",
    "ListEntitiesResponse",
    "ListEntriesRequest",
    "ListEntriesResponse",
    "ListEntryGroupsRequest",
    "ListEntryGroupsResponse",
    "ListEntryTypesRequest",
    "ListEntryTypesResponse",
    "ListEnvironmentsRequest",
    "ListEnvironmentsResponse",
    "ListGlossariesRequest",
    "ListGlossariesResponse",
    "ListGlossaryCategoriesRequest",
    "ListGlossaryCategoriesResponse",
    "ListGlossaryTermsRequest",
    "ListGlossaryTermsResponse",
    "ListJobsRequest",
    "ListJobsResponse",
    "ListLakeActionsRequest",
    "ListLakesRequest",
    "ListLakesResponse",
    "ListMetadataJobsRequest",
    "ListMetadataJobsResponse",
    "ListPartitionsRequest",
    "ListPartitionsResponse",
    "ListSessionsRequest",
    "ListSessionsResponse",
    "ListTasksRequest",
    "ListTasksResponse",
    "ListZoneActionsRequest",
    "ListZonesRequest",
    "ListZonesResponse",
    "LookupEntryRequest",
    "MetadataJob",
    "MetadataServiceClient",
    "OperationMetadata",
    "Partition",
    "ResourceAccessSpec",
    "RunDataScanRequest",
    "RunDataScanResponse",
    "RunTaskRequest",
    "RunTaskResponse",
    "ScannedData",
    "Schema",
    "SearchEntriesRequest",
    "SearchEntriesResponse",
    "SearchEntriesResult",
    "Session",
    "SessionEvent",
    "State",
    "StorageAccess",
    "StorageFormat",
    "StorageSystem",
    "Task",
    "TransferStatus",
    "Trigger",
    "UpdateAspectTypeRequest",
    "UpdateAssetRequest",
    "UpdateContentRequest",
    "UpdateDataAttributeBindingRequest",
    "UpdateDataAttributeRequest",
    "UpdateDataScanRequest",
    "UpdateDataTaxonomyRequest",
    "UpdateEncryptionConfigRequest",
    "UpdateEntityRequest",
    "UpdateEntryGroupRequest",
    "UpdateEntryRequest",
    "UpdateEntryTypeRequest",
    "UpdateEnvironmentRequest",
    "UpdateGlossaryCategoryRequest",
    "UpdateGlossaryRequest",
    "UpdateGlossaryTermRequest",
    "UpdateLakeRequest",
    "UpdateTaskRequest",
    "UpdateZoneRequest",
    "Zone",
)
