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
from google.cloud.migrationcenter import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.migrationcenter_v1.services.migration_center.client import MigrationCenterClient
from google.cloud.migrationcenter_v1.services.migration_center.async_client import MigrationCenterAsyncClient

from google.cloud.migrationcenter_v1.types.migrationcenter import AddAssetsToGroupRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import AggregateAssetsValuesRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import AggregateAssetsValuesResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import Aggregation
from google.cloud.migrationcenter_v1.types.migrationcenter import AggregationResult
from google.cloud.migrationcenter_v1.types.migrationcenter import Asset
from google.cloud.migrationcenter_v1.types.migrationcenter import AssetFrame
from google.cloud.migrationcenter_v1.types.migrationcenter import AssetList
from google.cloud.migrationcenter_v1.types.migrationcenter import AssetPerformanceData
from google.cloud.migrationcenter_v1.types.migrationcenter import AwsEc2PlatformDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import AzureVmPlatformDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import BatchDeleteAssetsRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import BatchUpdateAssetsRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import BatchUpdateAssetsResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import BiosDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import ComputeEngineMigrationTarget
from google.cloud.migrationcenter_v1.types.migrationcenter import ComputeEnginePreferences
from google.cloud.migrationcenter_v1.types.migrationcenter import ComputeEngineShapeDescriptor
from google.cloud.migrationcenter_v1.types.migrationcenter import CpuUsageSample
from google.cloud.migrationcenter_v1.types.migrationcenter import CreateGroupRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import CreateImportDataFileRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import CreateImportJobRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import CreatePreferenceSetRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import CreateReportConfigRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import CreateReportRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import CreateSourceRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import DailyResourceUsageAggregation
from google.cloud.migrationcenter_v1.types.migrationcenter import DeleteAssetRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import DeleteGroupRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import DeleteImportDataFileRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import DeleteImportJobRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import DeletePreferenceSetRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import DeleteReportConfigRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import DeleteReportRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import DeleteSourceRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import DiskEntry
from google.cloud.migrationcenter_v1.types.migrationcenter import DiskEntryList
from google.cloud.migrationcenter_v1.types.migrationcenter import DiskPartition
from google.cloud.migrationcenter_v1.types.migrationcenter import DiskPartitionList
from google.cloud.migrationcenter_v1.types.migrationcenter import DiskUsageSample
from google.cloud.migrationcenter_v1.types.migrationcenter import ErrorFrame
from google.cloud.migrationcenter_v1.types.migrationcenter import ExecutionReport
from google.cloud.migrationcenter_v1.types.migrationcenter import FileValidationReport
from google.cloud.migrationcenter_v1.types.migrationcenter import FitDescriptor
from google.cloud.migrationcenter_v1.types.migrationcenter import Frames
from google.cloud.migrationcenter_v1.types.migrationcenter import FrameViolationEntry
from google.cloud.migrationcenter_v1.types.migrationcenter import FstabEntry
from google.cloud.migrationcenter_v1.types.migrationcenter import FstabEntryList
from google.cloud.migrationcenter_v1.types.migrationcenter import GenericPlatformDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import GetAssetRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import GetErrorFrameRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import GetGroupRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import GetImportDataFileRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import GetImportJobRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import GetPreferenceSetRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import GetReportConfigRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import GetReportRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import GetSettingsRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import GetSourceRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import Group
from google.cloud.migrationcenter_v1.types.migrationcenter import GuestConfigDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import GuestInstalledApplication
from google.cloud.migrationcenter_v1.types.migrationcenter import GuestInstalledApplicationList
from google.cloud.migrationcenter_v1.types.migrationcenter import GuestOsDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import GuestRuntimeDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import HostsEntry
from google.cloud.migrationcenter_v1.types.migrationcenter import HostsEntryList
from google.cloud.migrationcenter_v1.types.migrationcenter import ImportDataFile
from google.cloud.migrationcenter_v1.types.migrationcenter import ImportError
from google.cloud.migrationcenter_v1.types.migrationcenter import ImportJob
from google.cloud.migrationcenter_v1.types.migrationcenter import ImportRowError
from google.cloud.migrationcenter_v1.types.migrationcenter import Insight
from google.cloud.migrationcenter_v1.types.migrationcenter import InsightList
from google.cloud.migrationcenter_v1.types.migrationcenter import ListAssetsRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ListAssetsResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import ListErrorFramesRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ListErrorFramesResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import ListGroupsRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ListGroupsResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import ListImportDataFilesRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ListImportDataFilesResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import ListImportJobsRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ListImportJobsResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import ListPreferenceSetsRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ListPreferenceSetsResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import ListReportConfigsRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ListReportConfigsResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import ListReportsRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ListReportsResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import ListSourcesRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ListSourcesResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import MachineArchitectureDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import MachineDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import MachineDiskDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import MachineNetworkDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import MachinePreferences
from google.cloud.migrationcenter_v1.types.migrationcenter import MachineSeries
from google.cloud.migrationcenter_v1.types.migrationcenter import MemoryUsageSample
from google.cloud.migrationcenter_v1.types.migrationcenter import MigrationInsight
from google.cloud.migrationcenter_v1.types.migrationcenter import NetworkAdapterDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import NetworkAdapterList
from google.cloud.migrationcenter_v1.types.migrationcenter import NetworkAddress
from google.cloud.migrationcenter_v1.types.migrationcenter import NetworkAddressList
from google.cloud.migrationcenter_v1.types.migrationcenter import NetworkConnection
from google.cloud.migrationcenter_v1.types.migrationcenter import NetworkConnectionList
from google.cloud.migrationcenter_v1.types.migrationcenter import NetworkUsageSample
from google.cloud.migrationcenter_v1.types.migrationcenter import NfsExport
from google.cloud.migrationcenter_v1.types.migrationcenter import NfsExportList
from google.cloud.migrationcenter_v1.types.migrationcenter import OpenFileDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import OpenFileList
from google.cloud.migrationcenter_v1.types.migrationcenter import OperationMetadata
from google.cloud.migrationcenter_v1.types.migrationcenter import PerformanceSample
from google.cloud.migrationcenter_v1.types.migrationcenter import PhysicalPlatformDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import PlatformDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import PreferenceSet
from google.cloud.migrationcenter_v1.types.migrationcenter import RegionPreferences
from google.cloud.migrationcenter_v1.types.migrationcenter import RemoveAssetsFromGroupRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import Report
from google.cloud.migrationcenter_v1.types.migrationcenter import ReportAssetFramesRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ReportAssetFramesResponse
from google.cloud.migrationcenter_v1.types.migrationcenter import ReportConfig
from google.cloud.migrationcenter_v1.types.migrationcenter import ReportSummary
from google.cloud.migrationcenter_v1.types.migrationcenter import RunImportJobRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import RunningProcess
from google.cloud.migrationcenter_v1.types.migrationcenter import RunningProcessList
from google.cloud.migrationcenter_v1.types.migrationcenter import RunningService
from google.cloud.migrationcenter_v1.types.migrationcenter import RunningServiceList
from google.cloud.migrationcenter_v1.types.migrationcenter import RuntimeNetworkInfo
from google.cloud.migrationcenter_v1.types.migrationcenter import Settings
from google.cloud.migrationcenter_v1.types.migrationcenter import Source
from google.cloud.migrationcenter_v1.types.migrationcenter import UpdateAssetRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import UpdateGroupRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import UpdateImportJobRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import UpdatePreferenceSetRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import UpdateSettingsRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import UpdateSourceRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import UploadFileInfo
from google.cloud.migrationcenter_v1.types.migrationcenter import ValidateImportJobRequest
from google.cloud.migrationcenter_v1.types.migrationcenter import ValidationReport
from google.cloud.migrationcenter_v1.types.migrationcenter import VirtualMachinePreferences
from google.cloud.migrationcenter_v1.types.migrationcenter import VmwareDiskConfig
from google.cloud.migrationcenter_v1.types.migrationcenter import VmwarePlatformDetails
from google.cloud.migrationcenter_v1.types.migrationcenter import AssetView
from google.cloud.migrationcenter_v1.types.migrationcenter import CommitmentPlan
from google.cloud.migrationcenter_v1.types.migrationcenter import ErrorFrameView
from google.cloud.migrationcenter_v1.types.migrationcenter import ImportJobFormat
from google.cloud.migrationcenter_v1.types.migrationcenter import ImportJobView
from google.cloud.migrationcenter_v1.types.migrationcenter import LicenseType
from google.cloud.migrationcenter_v1.types.migrationcenter import OperatingSystemFamily
from google.cloud.migrationcenter_v1.types.migrationcenter import PersistentDiskType
from google.cloud.migrationcenter_v1.types.migrationcenter import ReportView
from google.cloud.migrationcenter_v1.types.migrationcenter import SizingOptimizationStrategy

__all__ = ('MigrationCenterClient',
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
    'AwsEc2PlatformDetails',
    'AzureVmPlatformDetails',
    'BatchDeleteAssetsRequest',
    'BatchUpdateAssetsRequest',
    'BatchUpdateAssetsResponse',
    'BiosDetails',
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
    'ExecutionReport',
    'FileValidationReport',
    'FitDescriptor',
    'Frames',
    'FrameViolationEntry',
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
    'ImportRowError',
    'Insight',
    'InsightList',
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
    'OperationMetadata',
    'PerformanceSample',
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
    'RunImportJobRequest',
    'RunningProcess',
    'RunningProcessList',
    'RunningService',
    'RunningServiceList',
    'RuntimeNetworkInfo',
    'Settings',
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
    'AssetView',
    'CommitmentPlan',
    'ErrorFrameView',
    'ImportJobFormat',
    'ImportJobView',
    'LicenseType',
    'OperatingSystemFamily',
    'PersistentDiskType',
    'ReportView',
    'SizingOptimizationStrategy',
)
