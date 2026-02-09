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

from google.cloud.clouddms_v1 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.data_migration_service import (
    DataMigrationServiceAsyncClient,
    DataMigrationServiceClient,
)
from .types.clouddms import (
    ApplyConversionWorkspaceRequest,
    CommitConversionWorkspaceRequest,
    ConvertConversionWorkspaceRequest,
    CreateConnectionProfileRequest,
    CreateConversionWorkspaceRequest,
    CreateMappingRuleRequest,
    CreateMigrationJobRequest,
    CreatePrivateConnectionRequest,
    DatabaseEntityView,
    DeleteConnectionProfileRequest,
    DeleteConversionWorkspaceRequest,
    DeleteMappingRuleRequest,
    DeleteMigrationJobRequest,
    DeletePrivateConnectionRequest,
    DescribeConversionWorkspaceRevisionsRequest,
    DescribeConversionWorkspaceRevisionsResponse,
    DescribeDatabaseEntitiesRequest,
    DescribeDatabaseEntitiesResponse,
    FetchStaticIpsRequest,
    FetchStaticIpsResponse,
    GenerateSshScriptRequest,
    GenerateTcpProxyScriptRequest,
    GetConnectionProfileRequest,
    GetConversionWorkspaceRequest,
    GetMappingRuleRequest,
    GetMigrationJobRequest,
    GetPrivateConnectionRequest,
    ImportMappingRulesRequest,
    ListConnectionProfilesRequest,
    ListConnectionProfilesResponse,
    ListConversionWorkspacesRequest,
    ListConversionWorkspacesResponse,
    ListMappingRulesRequest,
    ListMappingRulesResponse,
    ListMigrationJobsRequest,
    ListMigrationJobsResponse,
    ListPrivateConnectionsRequest,
    ListPrivateConnectionsResponse,
    OperationMetadata,
    PromoteMigrationJobRequest,
    RestartMigrationJobRequest,
    ResumeMigrationJobRequest,
    RollbackConversionWorkspaceRequest,
    SearchBackgroundJobsRequest,
    SearchBackgroundJobsResponse,
    SeedConversionWorkspaceRequest,
    SshScript,
    StartMigrationJobRequest,
    StopMigrationJobRequest,
    TcpProxyScript,
    UpdateConnectionProfileRequest,
    UpdateConversionWorkspaceRequest,
    UpdateMigrationJobRequest,
    VerifyMigrationJobRequest,
    VmCreationConfig,
    VmSelectionConfig,
)
from .types.clouddms_resources import (
    AlloyDbConnectionProfile,
    AlloyDbSettings,
    CloudSqlConnectionProfile,
    CloudSqlSettings,
    ConnectionProfile,
    ConversionWorkspaceInfo,
    DatabaseEngine,
    DatabaseProvider,
    DatabaseType,
    ForwardSshTunnelConnectivity,
    MigrationJob,
    MigrationJobVerificationError,
    MySqlConnectionProfile,
    NetworkArchitecture,
    OracleConnectionProfile,
    PostgreSqlConnectionProfile,
    PrivateConnection,
    PrivateConnectivity,
    PrivateServiceConnectConnectivity,
    ReverseSshConnectivity,
    SqlAclEntry,
    SqlIpConfig,
    SslConfig,
    StaticIpConnectivity,
    StaticServiceIpConnectivity,
    VpcPeeringConfig,
    VpcPeeringConnectivity,
)
from .types.conversionworkspace_resources import (
    ApplyHash,
    AssignSpecificValue,
    BackgroundJobLogEntry,
    BackgroundJobType,
    ColumnEntity,
    ConditionalColumnSetValue,
    ConstraintEntity,
    ConversionWorkspace,
    ConvertRowIdToColumn,
    DatabaseEngineInfo,
    DatabaseEntity,
    DatabaseEntityType,
    DatabaseInstanceEntity,
    DoubleComparisonFilter,
    EntityDdl,
    EntityIssue,
    EntityMapping,
    EntityMappingLogEntry,
    EntityMove,
    EntityNameTransformation,
    FilterTableColumns,
    FunctionEntity,
    ImportRulesFileFormat,
    IndexEntity,
    IntComparisonFilter,
    MappingRule,
    MappingRuleFilter,
    MaterializedViewEntity,
    MultiColumnDatatypeChange,
    MultiEntityRename,
    NumericFilterOption,
    PackageEntity,
    RoundToScale,
    SchemaEntity,
    SequenceEntity,
    SetTablePrimaryKey,
    SingleColumnChange,
    SingleEntityRename,
    SinglePackageChange,
    SourceNumericFilter,
    SourceSqlChange,
    SourceTextFilter,
    StoredProcedureEntity,
    SynonymEntity,
    TableEntity,
    TriggerEntity,
    UDTEntity,
    ValueComparison,
    ValueListFilter,
    ValuePresentInList,
    ValueTransformation,
    ViewEntity,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.clouddms_v1")  # type: ignore
    api_core.check_dependency_versions("google.cloud.clouddms_v1")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.clouddms_v1"
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
    "DataMigrationServiceAsyncClient",
    "AlloyDbConnectionProfile",
    "AlloyDbSettings",
    "ApplyConversionWorkspaceRequest",
    "ApplyHash",
    "AssignSpecificValue",
    "BackgroundJobLogEntry",
    "BackgroundJobType",
    "CloudSqlConnectionProfile",
    "CloudSqlSettings",
    "ColumnEntity",
    "CommitConversionWorkspaceRequest",
    "ConditionalColumnSetValue",
    "ConnectionProfile",
    "ConstraintEntity",
    "ConversionWorkspace",
    "ConversionWorkspaceInfo",
    "ConvertConversionWorkspaceRequest",
    "ConvertRowIdToColumn",
    "CreateConnectionProfileRequest",
    "CreateConversionWorkspaceRequest",
    "CreateMappingRuleRequest",
    "CreateMigrationJobRequest",
    "CreatePrivateConnectionRequest",
    "DataMigrationServiceClient",
    "DatabaseEngine",
    "DatabaseEngineInfo",
    "DatabaseEntity",
    "DatabaseEntityType",
    "DatabaseEntityView",
    "DatabaseInstanceEntity",
    "DatabaseProvider",
    "DatabaseType",
    "DeleteConnectionProfileRequest",
    "DeleteConversionWorkspaceRequest",
    "DeleteMappingRuleRequest",
    "DeleteMigrationJobRequest",
    "DeletePrivateConnectionRequest",
    "DescribeConversionWorkspaceRevisionsRequest",
    "DescribeConversionWorkspaceRevisionsResponse",
    "DescribeDatabaseEntitiesRequest",
    "DescribeDatabaseEntitiesResponse",
    "DoubleComparisonFilter",
    "EntityDdl",
    "EntityIssue",
    "EntityMapping",
    "EntityMappingLogEntry",
    "EntityMove",
    "EntityNameTransformation",
    "FetchStaticIpsRequest",
    "FetchStaticIpsResponse",
    "FilterTableColumns",
    "ForwardSshTunnelConnectivity",
    "FunctionEntity",
    "GenerateSshScriptRequest",
    "GenerateTcpProxyScriptRequest",
    "GetConnectionProfileRequest",
    "GetConversionWorkspaceRequest",
    "GetMappingRuleRequest",
    "GetMigrationJobRequest",
    "GetPrivateConnectionRequest",
    "ImportMappingRulesRequest",
    "ImportRulesFileFormat",
    "IndexEntity",
    "IntComparisonFilter",
    "ListConnectionProfilesRequest",
    "ListConnectionProfilesResponse",
    "ListConversionWorkspacesRequest",
    "ListConversionWorkspacesResponse",
    "ListMappingRulesRequest",
    "ListMappingRulesResponse",
    "ListMigrationJobsRequest",
    "ListMigrationJobsResponse",
    "ListPrivateConnectionsRequest",
    "ListPrivateConnectionsResponse",
    "MappingRule",
    "MappingRuleFilter",
    "MaterializedViewEntity",
    "MigrationJob",
    "MigrationJobVerificationError",
    "MultiColumnDatatypeChange",
    "MultiEntityRename",
    "MySqlConnectionProfile",
    "NetworkArchitecture",
    "NumericFilterOption",
    "OperationMetadata",
    "OracleConnectionProfile",
    "PackageEntity",
    "PostgreSqlConnectionProfile",
    "PrivateConnection",
    "PrivateConnectivity",
    "PrivateServiceConnectConnectivity",
    "PromoteMigrationJobRequest",
    "RestartMigrationJobRequest",
    "ResumeMigrationJobRequest",
    "ReverseSshConnectivity",
    "RollbackConversionWorkspaceRequest",
    "RoundToScale",
    "SchemaEntity",
    "SearchBackgroundJobsRequest",
    "SearchBackgroundJobsResponse",
    "SeedConversionWorkspaceRequest",
    "SequenceEntity",
    "SetTablePrimaryKey",
    "SingleColumnChange",
    "SingleEntityRename",
    "SinglePackageChange",
    "SourceNumericFilter",
    "SourceSqlChange",
    "SourceTextFilter",
    "SqlAclEntry",
    "SqlIpConfig",
    "SshScript",
    "SslConfig",
    "StartMigrationJobRequest",
    "StaticIpConnectivity",
    "StaticServiceIpConnectivity",
    "StopMigrationJobRequest",
    "StoredProcedureEntity",
    "SynonymEntity",
    "TableEntity",
    "TcpProxyScript",
    "TriggerEntity",
    "UDTEntity",
    "UpdateConnectionProfileRequest",
    "UpdateConversionWorkspaceRequest",
    "UpdateMigrationJobRequest",
    "ValueComparison",
    "ValueListFilter",
    "ValuePresentInList",
    "ValueTransformation",
    "VerifyMigrationJobRequest",
    "ViewEntity",
    "VmCreationConfig",
    "VmSelectionConfig",
    "VpcPeeringConfig",
    "VpcPeeringConnectivity",
)
