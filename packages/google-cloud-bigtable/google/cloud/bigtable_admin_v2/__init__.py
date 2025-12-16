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
from google.cloud.bigtable_admin_v2 import gapic_version as package_version

import google.api_core as api_core
import sys

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.bigtable_instance_admin import BigtableInstanceAdminClient
from .services.bigtable_instance_admin import BigtableInstanceAdminAsyncClient
from .services.bigtable_table_admin import BaseBigtableTableAdminClient
from .services.bigtable_table_admin import BaseBigtableTableAdminAsyncClient

from .types.bigtable_instance_admin import CreateAppProfileRequest
from .types.bigtable_instance_admin import CreateClusterMetadata
from .types.bigtable_instance_admin import CreateClusterRequest
from .types.bigtable_instance_admin import CreateInstanceMetadata
from .types.bigtable_instance_admin import CreateInstanceRequest
from .types.bigtable_instance_admin import CreateLogicalViewMetadata
from .types.bigtable_instance_admin import CreateLogicalViewRequest
from .types.bigtable_instance_admin import CreateMaterializedViewMetadata
from .types.bigtable_instance_admin import CreateMaterializedViewRequest
from .types.bigtable_instance_admin import DeleteAppProfileRequest
from .types.bigtable_instance_admin import DeleteClusterRequest
from .types.bigtable_instance_admin import DeleteInstanceRequest
from .types.bigtable_instance_admin import DeleteLogicalViewRequest
from .types.bigtable_instance_admin import DeleteMaterializedViewRequest
from .types.bigtable_instance_admin import GetAppProfileRequest
from .types.bigtable_instance_admin import GetClusterRequest
from .types.bigtable_instance_admin import GetInstanceRequest
from .types.bigtable_instance_admin import GetLogicalViewRequest
from .types.bigtable_instance_admin import GetMaterializedViewRequest
from .types.bigtable_instance_admin import ListAppProfilesRequest
from .types.bigtable_instance_admin import ListAppProfilesResponse
from .types.bigtable_instance_admin import ListClustersRequest
from .types.bigtable_instance_admin import ListClustersResponse
from .types.bigtable_instance_admin import ListHotTabletsRequest
from .types.bigtable_instance_admin import ListHotTabletsResponse
from .types.bigtable_instance_admin import ListInstancesRequest
from .types.bigtable_instance_admin import ListInstancesResponse
from .types.bigtable_instance_admin import ListLogicalViewsRequest
from .types.bigtable_instance_admin import ListLogicalViewsResponse
from .types.bigtable_instance_admin import ListMaterializedViewsRequest
from .types.bigtable_instance_admin import ListMaterializedViewsResponse
from .types.bigtable_instance_admin import PartialUpdateClusterMetadata
from .types.bigtable_instance_admin import PartialUpdateClusterRequest
from .types.bigtable_instance_admin import PartialUpdateInstanceRequest
from .types.bigtable_instance_admin import UpdateAppProfileMetadata
from .types.bigtable_instance_admin import UpdateAppProfileRequest
from .types.bigtable_instance_admin import UpdateClusterMetadata
from .types.bigtable_instance_admin import UpdateInstanceMetadata
from .types.bigtable_instance_admin import UpdateLogicalViewMetadata
from .types.bigtable_instance_admin import UpdateLogicalViewRequest
from .types.bigtable_instance_admin import UpdateMaterializedViewMetadata
from .types.bigtable_instance_admin import UpdateMaterializedViewRequest
from .types.bigtable_table_admin import CheckConsistencyRequest
from .types.bigtable_table_admin import CheckConsistencyResponse
from .types.bigtable_table_admin import CopyBackupMetadata
from .types.bigtable_table_admin import CopyBackupRequest
from .types.bigtable_table_admin import CreateAuthorizedViewMetadata
from .types.bigtable_table_admin import CreateAuthorizedViewRequest
from .types.bigtable_table_admin import CreateBackupMetadata
from .types.bigtable_table_admin import CreateBackupRequest
from .types.bigtable_table_admin import CreateSchemaBundleMetadata
from .types.bigtable_table_admin import CreateSchemaBundleRequest
from .types.bigtable_table_admin import CreateTableFromSnapshotMetadata
from .types.bigtable_table_admin import CreateTableFromSnapshotRequest
from .types.bigtable_table_admin import CreateTableRequest
from .types.bigtable_table_admin import DataBoostReadLocalWrites
from .types.bigtable_table_admin import DeleteAuthorizedViewRequest
from .types.bigtable_table_admin import DeleteBackupRequest
from .types.bigtable_table_admin import DeleteSchemaBundleRequest
from .types.bigtable_table_admin import DeleteSnapshotRequest
from .types.bigtable_table_admin import DeleteTableRequest
from .types.bigtable_table_admin import DropRowRangeRequest
from .types.bigtable_table_admin import GenerateConsistencyTokenRequest
from .types.bigtable_table_admin import GenerateConsistencyTokenResponse
from .types.bigtable_table_admin import GetAuthorizedViewRequest
from .types.bigtable_table_admin import GetBackupRequest
from .types.bigtable_table_admin import GetSchemaBundleRequest
from .types.bigtable_table_admin import GetSnapshotRequest
from .types.bigtable_table_admin import GetTableRequest
from .types.bigtable_table_admin import ListAuthorizedViewsRequest
from .types.bigtable_table_admin import ListAuthorizedViewsResponse
from .types.bigtable_table_admin import ListBackupsRequest
from .types.bigtable_table_admin import ListBackupsResponse
from .types.bigtable_table_admin import ListSchemaBundlesRequest
from .types.bigtable_table_admin import ListSchemaBundlesResponse
from .types.bigtable_table_admin import ListSnapshotsRequest
from .types.bigtable_table_admin import ListSnapshotsResponse
from .types.bigtable_table_admin import ListTablesRequest
from .types.bigtable_table_admin import ListTablesResponse
from .types.bigtable_table_admin import ModifyColumnFamiliesRequest
from .types.bigtable_table_admin import OptimizeRestoredTableMetadata
from .types.bigtable_table_admin import RestoreTableMetadata
from .types.bigtable_table_admin import RestoreTableRequest
from .types.bigtable_table_admin import SnapshotTableMetadata
from .types.bigtable_table_admin import SnapshotTableRequest
from .types.bigtable_table_admin import StandardReadRemoteWrites
from .types.bigtable_table_admin import UndeleteTableMetadata
from .types.bigtable_table_admin import UndeleteTableRequest
from .types.bigtable_table_admin import UpdateAuthorizedViewMetadata
from .types.bigtable_table_admin import UpdateAuthorizedViewRequest
from .types.bigtable_table_admin import UpdateBackupRequest
from .types.bigtable_table_admin import UpdateSchemaBundleMetadata
from .types.bigtable_table_admin import UpdateSchemaBundleRequest
from .types.bigtable_table_admin import UpdateTableMetadata
from .types.bigtable_table_admin import UpdateTableRequest
from .types.common import OperationProgress
from .types.common import StorageType
from .types.instance import AppProfile
from .types.instance import AutoscalingLimits
from .types.instance import AutoscalingTargets
from .types.instance import Cluster
from .types.instance import HotTablet
from .types.instance import Instance
from .types.instance import LogicalView
from .types.instance import MaterializedView
from .types.table import AuthorizedView
from .types.table import Backup
from .types.table import BackupInfo
from .types.table import ChangeStreamConfig
from .types.table import ColumnFamily
from .types.table import EncryptionInfo
from .types.table import GcRule
from .types.table import ProtoSchema
from .types.table import RestoreInfo
from .types.table import SchemaBundle
from .types.table import Snapshot
from .types.table import Table
from .types.table import RestoreSourceType
from .types.types import Type

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.bigtable_admin_v2")  # type: ignore
    api_core.check_dependency_versions("google.cloud.bigtable_admin_v2")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import warnings
        import sys

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.bigtable_admin_v2"
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
    "BaseBigtableTableAdminAsyncClient",
    "BigtableInstanceAdminAsyncClient",
    "AppProfile",
    "AuthorizedView",
    "AutoscalingLimits",
    "AutoscalingTargets",
    "Backup",
    "BackupInfo",
    "BaseBigtableTableAdminClient",
    "BigtableInstanceAdminClient",
    "ChangeStreamConfig",
    "CheckConsistencyRequest",
    "CheckConsistencyResponse",
    "Cluster",
    "ColumnFamily",
    "CopyBackupMetadata",
    "CopyBackupRequest",
    "CreateAppProfileRequest",
    "CreateAuthorizedViewMetadata",
    "CreateAuthorizedViewRequest",
    "CreateBackupMetadata",
    "CreateBackupRequest",
    "CreateClusterMetadata",
    "CreateClusterRequest",
    "CreateInstanceMetadata",
    "CreateInstanceRequest",
    "CreateLogicalViewMetadata",
    "CreateLogicalViewRequest",
    "CreateMaterializedViewMetadata",
    "CreateMaterializedViewRequest",
    "CreateSchemaBundleMetadata",
    "CreateSchemaBundleRequest",
    "CreateTableFromSnapshotMetadata",
    "CreateTableFromSnapshotRequest",
    "CreateTableRequest",
    "DataBoostReadLocalWrites",
    "DeleteAppProfileRequest",
    "DeleteAuthorizedViewRequest",
    "DeleteBackupRequest",
    "DeleteClusterRequest",
    "DeleteInstanceRequest",
    "DeleteLogicalViewRequest",
    "DeleteMaterializedViewRequest",
    "DeleteSchemaBundleRequest",
    "DeleteSnapshotRequest",
    "DeleteTableRequest",
    "DropRowRangeRequest",
    "EncryptionInfo",
    "GcRule",
    "GenerateConsistencyTokenRequest",
    "GenerateConsistencyTokenResponse",
    "GetAppProfileRequest",
    "GetAuthorizedViewRequest",
    "GetBackupRequest",
    "GetClusterRequest",
    "GetInstanceRequest",
    "GetLogicalViewRequest",
    "GetMaterializedViewRequest",
    "GetSchemaBundleRequest",
    "GetSnapshotRequest",
    "GetTableRequest",
    "HotTablet",
    "Instance",
    "ListAppProfilesRequest",
    "ListAppProfilesResponse",
    "ListAuthorizedViewsRequest",
    "ListAuthorizedViewsResponse",
    "ListBackupsRequest",
    "ListBackupsResponse",
    "ListClustersRequest",
    "ListClustersResponse",
    "ListHotTabletsRequest",
    "ListHotTabletsResponse",
    "ListInstancesRequest",
    "ListInstancesResponse",
    "ListLogicalViewsRequest",
    "ListLogicalViewsResponse",
    "ListMaterializedViewsRequest",
    "ListMaterializedViewsResponse",
    "ListSchemaBundlesRequest",
    "ListSchemaBundlesResponse",
    "ListSnapshotsRequest",
    "ListSnapshotsResponse",
    "ListTablesRequest",
    "ListTablesResponse",
    "LogicalView",
    "MaterializedView",
    "ModifyColumnFamiliesRequest",
    "OperationProgress",
    "OptimizeRestoredTableMetadata",
    "PartialUpdateClusterMetadata",
    "PartialUpdateClusterRequest",
    "PartialUpdateInstanceRequest",
    "ProtoSchema",
    "RestoreInfo",
    "RestoreSourceType",
    "RestoreTableMetadata",
    "RestoreTableRequest",
    "SchemaBundle",
    "Snapshot",
    "SnapshotTableMetadata",
    "SnapshotTableRequest",
    "StandardReadRemoteWrites",
    "StorageType",
    "Table",
    "Type",
    "UndeleteTableMetadata",
    "UndeleteTableRequest",
    "UpdateAppProfileMetadata",
    "UpdateAppProfileRequest",
    "UpdateAuthorizedViewMetadata",
    "UpdateAuthorizedViewRequest",
    "UpdateBackupRequest",
    "UpdateClusterMetadata",
    "UpdateInstanceMetadata",
    "UpdateLogicalViewMetadata",
    "UpdateLogicalViewRequest",
    "UpdateMaterializedViewMetadata",
    "UpdateMaterializedViewRequest",
    "UpdateSchemaBundleMetadata",
    "UpdateSchemaBundleRequest",
    "UpdateTableMetadata",
    "UpdateTableRequest",
)

from .overlay import *  # noqa: F403

__all__ += overlay.__all__  # noqa: F405
