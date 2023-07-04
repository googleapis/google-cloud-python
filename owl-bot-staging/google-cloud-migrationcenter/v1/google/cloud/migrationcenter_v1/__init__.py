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
from google.cloud.migrationcenter_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.migration_center import MigrationCenterClient
from .services.migration_center import MigrationCenterAsyncClient

from .types.migrationcenter import AddAssetsToGroupRequest
from .types.migrationcenter import AggregateAssetsValuesRequest
from .types.migrationcenter import AggregateAssetsValuesResponse
from .types.migrationcenter import Aggregation
from .types.migrationcenter import AggregationResult
from .types.migrationcenter import Asset
from .types.migrationcenter import AssetFrame
from .types.migrationcenter import AssetList
from .types.migrationcenter import AssetPerformanceData
from .types.migrationcenter import AwsEc2PlatformDetails
from .types.migrationcenter import AzureVmPlatformDetails
from .types.migrationcenter import BatchDeleteAssetsRequest
from .types.migrationcenter import BatchUpdateAssetsRequest
from .types.migrationcenter import BatchUpdateAssetsResponse
from .types.migrationcenter import BiosDetails
from .types.migrationcenter import ComputeEngineMigrationTarget
from .types.migrationcenter import ComputeEnginePreferences
from .types.migrationcenter import ComputeEngineShapeDescriptor
from .types.migrationcenter import CpuUsageSample
from .types.migrationcenter import CreateGroupRequest
from .types.migrationcenter import CreateImportDataFileRequest
from .types.migrationcenter import CreateImportJobRequest
from .types.migrationcenter import CreatePreferenceSetRequest
from .types.migrationcenter import CreateReportConfigRequest
from .types.migrationcenter import CreateReportRequest
from .types.migrationcenter import CreateSourceRequest
from .types.migrationcenter import DailyResourceUsageAggregation
from .types.migrationcenter import DeleteAssetRequest
from .types.migrationcenter import DeleteGroupRequest
from .types.migrationcenter import DeleteImportDataFileRequest
from .types.migrationcenter import DeleteImportJobRequest
from .types.migrationcenter import DeletePreferenceSetRequest
from .types.migrationcenter import DeleteReportConfigRequest
from .types.migrationcenter import DeleteReportRequest
from .types.migrationcenter import DeleteSourceRequest
from .types.migrationcenter import DiskEntry
from .types.migrationcenter import DiskEntryList
from .types.migrationcenter import DiskPartition
from .types.migrationcenter import DiskPartitionList
from .types.migrationcenter import DiskUsageSample
from .types.migrationcenter import ErrorFrame
from .types.migrationcenter import ExecutionReport
from .types.migrationcenter import FileValidationReport
from .types.migrationcenter import FitDescriptor
from .types.migrationcenter import Frames
from .types.migrationcenter import FrameViolationEntry
from .types.migrationcenter import FstabEntry
from .types.migrationcenter import FstabEntryList
from .types.migrationcenter import GenericPlatformDetails
from .types.migrationcenter import GetAssetRequest
from .types.migrationcenter import GetErrorFrameRequest
from .types.migrationcenter import GetGroupRequest
from .types.migrationcenter import GetImportDataFileRequest
from .types.migrationcenter import GetImportJobRequest
from .types.migrationcenter import GetPreferenceSetRequest
from .types.migrationcenter import GetReportConfigRequest
from .types.migrationcenter import GetReportRequest
from .types.migrationcenter import GetSettingsRequest
from .types.migrationcenter import GetSourceRequest
from .types.migrationcenter import Group
from .types.migrationcenter import GuestConfigDetails
from .types.migrationcenter import GuestInstalledApplication
from .types.migrationcenter import GuestInstalledApplicationList
from .types.migrationcenter import GuestOsDetails
from .types.migrationcenter import GuestRuntimeDetails
from .types.migrationcenter import HostsEntry
from .types.migrationcenter import HostsEntryList
from .types.migrationcenter import ImportDataFile
from .types.migrationcenter import ImportError
from .types.migrationcenter import ImportJob
from .types.migrationcenter import ImportRowError
from .types.migrationcenter import Insight
from .types.migrationcenter import InsightList
from .types.migrationcenter import ListAssetsRequest
from .types.migrationcenter import ListAssetsResponse
from .types.migrationcenter import ListErrorFramesRequest
from .types.migrationcenter import ListErrorFramesResponse
from .types.migrationcenter import ListGroupsRequest
from .types.migrationcenter import ListGroupsResponse
from .types.migrationcenter import ListImportDataFilesRequest
from .types.migrationcenter import ListImportDataFilesResponse
from .types.migrationcenter import ListImportJobsRequest
from .types.migrationcenter import ListImportJobsResponse
from .types.migrationcenter import ListPreferenceSetsRequest
from .types.migrationcenter import ListPreferenceSetsResponse
from .types.migrationcenter import ListReportConfigsRequest
from .types.migrationcenter import ListReportConfigsResponse
from .types.migrationcenter import ListReportsRequest
from .types.migrationcenter import ListReportsResponse
from .types.migrationcenter import ListSourcesRequest
from .types.migrationcenter import ListSourcesResponse
from .types.migrationcenter import MachineArchitectureDetails
from .types.migrationcenter import MachineDetails
from .types.migrationcenter import MachineDiskDetails
from .types.migrationcenter import MachineNetworkDetails
from .types.migrationcenter import MachinePreferences
from .types.migrationcenter import MachineSeries
from .types.migrationcenter import MemoryUsageSample
from .types.migrationcenter import MigrationInsight
from .types.migrationcenter import NetworkAdapterDetails
from .types.migrationcenter import NetworkAdapterList
from .types.migrationcenter import NetworkAddress
from .types.migrationcenter import NetworkAddressList
from .types.migrationcenter import NetworkConnection
from .types.migrationcenter import NetworkConnectionList
from .types.migrationcenter import NetworkUsageSample
from .types.migrationcenter import NfsExport
from .types.migrationcenter import NfsExportList
from .types.migrationcenter import OpenFileDetails
from .types.migrationcenter import OpenFileList
from .types.migrationcenter import OperationMetadata
from .types.migrationcenter import PerformanceSample
from .types.migrationcenter import PhysicalPlatformDetails
from .types.migrationcenter import PlatformDetails
from .types.migrationcenter import PreferenceSet
from .types.migrationcenter import RegionPreferences
from .types.migrationcenter import RemoveAssetsFromGroupRequest
from .types.migrationcenter import Report
from .types.migrationcenter import ReportAssetFramesRequest
from .types.migrationcenter import ReportAssetFramesResponse
from .types.migrationcenter import ReportConfig
from .types.migrationcenter import ReportSummary
from .types.migrationcenter import RunImportJobRequest
from .types.migrationcenter import RunningProcess
from .types.migrationcenter import RunningProcessList
from .types.migrationcenter import RunningService
from .types.migrationcenter import RunningServiceList
from .types.migrationcenter import RuntimeNetworkInfo
from .types.migrationcenter import Settings
from .types.migrationcenter import Source
from .types.migrationcenter import UpdateAssetRequest
from .types.migrationcenter import UpdateGroupRequest
from .types.migrationcenter import UpdateImportJobRequest
from .types.migrationcenter import UpdatePreferenceSetRequest
from .types.migrationcenter import UpdateSettingsRequest
from .types.migrationcenter import UpdateSourceRequest
from .types.migrationcenter import UploadFileInfo
from .types.migrationcenter import ValidateImportJobRequest
from .types.migrationcenter import ValidationReport
from .types.migrationcenter import VirtualMachinePreferences
from .types.migrationcenter import VmwareDiskConfig
from .types.migrationcenter import VmwarePlatformDetails
from .types.migrationcenter import AssetView
from .types.migrationcenter import CommitmentPlan
from .types.migrationcenter import ErrorFrameView
from .types.migrationcenter import ImportJobFormat
from .types.migrationcenter import ImportJobView
from .types.migrationcenter import LicenseType
from .types.migrationcenter import OperatingSystemFamily
from .types.migrationcenter import PersistentDiskType
from .types.migrationcenter import ReportView
from .types.migrationcenter import SizingOptimizationStrategy

__all__ = (
    'MigrationCenterAsyncClient',
'AddAssetsToGroupRequest',
'AggregateAssetsValuesRequest',
'AggregateAssetsValuesResponse',
'Aggregation',
'AggregationResult',
'Asset',
'AssetFrame',
'AssetList',
'AssetPerformanceData',
'AssetView',
'AwsEc2PlatformDetails',
'AzureVmPlatformDetails',
'BatchDeleteAssetsRequest',
'BatchUpdateAssetsRequest',
'BatchUpdateAssetsResponse',
'BiosDetails',
'CommitmentPlan',
'ComputeEngineMigrationTarget',
'ComputeEnginePreferences',
'ComputeEngineShapeDescriptor',
'CpuUsageSample',
'CreateGroupRequest',
'CreateImportDataFileRequest',
'CreateImportJobRequest',
'CreatePreferenceSetRequest',
'CreateReportConfigRequest',
'CreateReportRequest',
'CreateSourceRequest',
'DailyResourceUsageAggregation',
'DeleteAssetRequest',
'DeleteGroupRequest',
'DeleteImportDataFileRequest',
'DeleteImportJobRequest',
'DeletePreferenceSetRequest',
'DeleteReportConfigRequest',
'DeleteReportRequest',
'DeleteSourceRequest',
'DiskEntry',
'DiskEntryList',
'DiskPartition',
'DiskPartitionList',
'DiskUsageSample',
'ErrorFrame',
'ErrorFrameView',
'ExecutionReport',
'FileValidationReport',
'FitDescriptor',
'FrameViolationEntry',
'Frames',
'FstabEntry',
'FstabEntryList',
'GenericPlatformDetails',
'GetAssetRequest',
'GetErrorFrameRequest',
'GetGroupRequest',
'GetImportDataFileRequest',
'GetImportJobRequest',
'GetPreferenceSetRequest',
'GetReportConfigRequest',
'GetReportRequest',
'GetSettingsRequest',
'GetSourceRequest',
'Group',
'GuestConfigDetails',
'GuestInstalledApplication',
'GuestInstalledApplicationList',
'GuestOsDetails',
'GuestRuntimeDetails',
'HostsEntry',
'HostsEntryList',
'ImportDataFile',
'ImportError',
'ImportJob',
'ImportJobFormat',
'ImportJobView',
'ImportRowError',
'Insight',
'InsightList',
'LicenseType',
'ListAssetsRequest',
'ListAssetsResponse',
'ListErrorFramesRequest',
'ListErrorFramesResponse',
'ListGroupsRequest',
'ListGroupsResponse',
'ListImportDataFilesRequest',
'ListImportDataFilesResponse',
'ListImportJobsRequest',
'ListImportJobsResponse',
'ListPreferenceSetsRequest',
'ListPreferenceSetsResponse',
'ListReportConfigsRequest',
'ListReportConfigsResponse',
'ListReportsRequest',
'ListReportsResponse',
'ListSourcesRequest',
'ListSourcesResponse',
'MachineArchitectureDetails',
'MachineDetails',
'MachineDiskDetails',
'MachineNetworkDetails',
'MachinePreferences',
'MachineSeries',
'MemoryUsageSample',
'MigrationCenterClient',
'MigrationInsight',
'NetworkAdapterDetails',
'NetworkAdapterList',
'NetworkAddress',
'NetworkAddressList',
'NetworkConnection',
'NetworkConnectionList',
'NetworkUsageSample',
'NfsExport',
'NfsExportList',
'OpenFileDetails',
'OpenFileList',
'OperatingSystemFamily',
'OperationMetadata',
'PerformanceSample',
'PersistentDiskType',
'PhysicalPlatformDetails',
'PlatformDetails',
'PreferenceSet',
'RegionPreferences',
'RemoveAssetsFromGroupRequest',
'Report',
'ReportAssetFramesRequest',
'ReportAssetFramesResponse',
'ReportConfig',
'ReportSummary',
'ReportView',
'RunImportJobRequest',
'RunningProcess',
'RunningProcessList',
'RunningService',
'RunningServiceList',
'RuntimeNetworkInfo',
'Settings',
'SizingOptimizationStrategy',
'Source',
'UpdateAssetRequest',
'UpdateGroupRequest',
'UpdateImportJobRequest',
'UpdatePreferenceSetRequest',
'UpdateSettingsRequest',
'UpdateSourceRequest',
'UploadFileInfo',
'ValidateImportJobRequest',
'ValidationReport',
'VirtualMachinePreferences',
'VmwareDiskConfig',
'VmwarePlatformDetails',
)
