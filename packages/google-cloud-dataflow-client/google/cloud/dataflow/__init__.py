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
from google.cloud.dataflow import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.dataflow_v1beta3.services.flex_templates_service.async_client import (
    FlexTemplatesServiceAsyncClient,
)
from google.cloud.dataflow_v1beta3.services.flex_templates_service.client import (
    FlexTemplatesServiceClient,
)
from google.cloud.dataflow_v1beta3.services.jobs_v1_beta3.async_client import (
    JobsV1Beta3AsyncClient,
)
from google.cloud.dataflow_v1beta3.services.jobs_v1_beta3.client import (
    JobsV1Beta3Client,
)
from google.cloud.dataflow_v1beta3.services.messages_v1_beta3.async_client import (
    MessagesV1Beta3AsyncClient,
)
from google.cloud.dataflow_v1beta3.services.messages_v1_beta3.client import (
    MessagesV1Beta3Client,
)
from google.cloud.dataflow_v1beta3.services.metrics_v1_beta3.async_client import (
    MetricsV1Beta3AsyncClient,
)
from google.cloud.dataflow_v1beta3.services.metrics_v1_beta3.client import (
    MetricsV1Beta3Client,
)
from google.cloud.dataflow_v1beta3.services.snapshots_v1_beta3.async_client import (
    SnapshotsV1Beta3AsyncClient,
)
from google.cloud.dataflow_v1beta3.services.snapshots_v1_beta3.client import (
    SnapshotsV1Beta3Client,
)
from google.cloud.dataflow_v1beta3.services.templates_service.async_client import (
    TemplatesServiceAsyncClient,
)
from google.cloud.dataflow_v1beta3.services.templates_service.client import (
    TemplatesServiceClient,
)
from google.cloud.dataflow_v1beta3.types.environment import (
    AutoscalingAlgorithm,
    AutoscalingSettings,
    DebugOptions,
    DefaultPackageSet,
    Disk,
    Environment,
    FlexResourceSchedulingGoal,
    JobType,
    Package,
    SdkHarnessContainerImage,
    ShuffleMode,
    TaskRunnerSettings,
    TeardownPolicy,
    WorkerIPAddressConfiguration,
    WorkerPool,
    WorkerSettings,
)
from google.cloud.dataflow_v1beta3.types.jobs import (
    BigQueryIODetails,
    BigTableIODetails,
    CheckActiveJobsRequest,
    CheckActiveJobsResponse,
    CreateJobRequest,
    DatastoreIODetails,
    DisplayData,
    ExecutionStageState,
    ExecutionStageSummary,
    FailedLocation,
    FileIODetails,
    GetJobRequest,
    Job,
    JobExecutionInfo,
    JobExecutionStageInfo,
    JobMetadata,
    JobState,
    JobView,
    KindType,
    ListJobsRequest,
    ListJobsResponse,
    PipelineDescription,
    PubSubIODetails,
    SdkVersion,
    SnapshotJobRequest,
    SpannerIODetails,
    Step,
    TransformSummary,
    UpdateJobRequest,
)
from google.cloud.dataflow_v1beta3.types.messages import (
    AutoscalingEvent,
    JobMessage,
    JobMessageImportance,
    ListJobMessagesRequest,
    ListJobMessagesResponse,
    StructuredMessage,
)
from google.cloud.dataflow_v1beta3.types.metrics import (
    ExecutionState,
    GetJobExecutionDetailsRequest,
    GetJobMetricsRequest,
    GetStageExecutionDetailsRequest,
    JobExecutionDetails,
    JobMetrics,
    MetricStructuredName,
    MetricUpdate,
    ProgressTimeseries,
    StageExecutionDetails,
    StageSummary,
    WorkerDetails,
    WorkItemDetails,
)
from google.cloud.dataflow_v1beta3.types.snapshots import (
    DeleteSnapshotRequest,
    DeleteSnapshotResponse,
    GetSnapshotRequest,
    ListSnapshotsRequest,
    ListSnapshotsResponse,
    PubsubSnapshotMetadata,
    Snapshot,
    SnapshotState,
)
from google.cloud.dataflow_v1beta3.types.streaming import (
    ComputationTopology,
    CustomSourceLocation,
    DataDiskAssignment,
    KeyRangeDataDiskAssignment,
    KeyRangeLocation,
    MountedDataDisk,
    PubsubLocation,
    StateFamilyConfig,
    StreamingApplianceSnapshotConfig,
    StreamingComputationRanges,
    StreamingSideInputLocation,
    StreamingStageLocation,
    StreamLocation,
    TopologyConfig,
)
from google.cloud.dataflow_v1beta3.types.templates import (
    ContainerSpec,
    CreateJobFromTemplateRequest,
    DynamicTemplateLaunchParams,
    FlexTemplateRuntimeEnvironment,
    GetTemplateRequest,
    GetTemplateResponse,
    InvalidTemplateParameters,
    LaunchFlexTemplateParameter,
    LaunchFlexTemplateRequest,
    LaunchFlexTemplateResponse,
    LaunchTemplateParameters,
    LaunchTemplateRequest,
    LaunchTemplateResponse,
    ParameterMetadata,
    ParameterType,
    RuntimeEnvironment,
    RuntimeMetadata,
    SDKInfo,
    TemplateMetadata,
)

__all__ = (
    "FlexTemplatesServiceClient",
    "FlexTemplatesServiceAsyncClient",
    "JobsV1Beta3Client",
    "JobsV1Beta3AsyncClient",
    "MessagesV1Beta3Client",
    "MessagesV1Beta3AsyncClient",
    "MetricsV1Beta3Client",
    "MetricsV1Beta3AsyncClient",
    "SnapshotsV1Beta3Client",
    "SnapshotsV1Beta3AsyncClient",
    "TemplatesServiceClient",
    "TemplatesServiceAsyncClient",
    "AutoscalingSettings",
    "DebugOptions",
    "Disk",
    "Environment",
    "Package",
    "SdkHarnessContainerImage",
    "TaskRunnerSettings",
    "WorkerPool",
    "WorkerSettings",
    "AutoscalingAlgorithm",
    "DefaultPackageSet",
    "FlexResourceSchedulingGoal",
    "JobType",
    "ShuffleMode",
    "TeardownPolicy",
    "WorkerIPAddressConfiguration",
    "BigQueryIODetails",
    "BigTableIODetails",
    "CheckActiveJobsRequest",
    "CheckActiveJobsResponse",
    "CreateJobRequest",
    "DatastoreIODetails",
    "DisplayData",
    "ExecutionStageState",
    "ExecutionStageSummary",
    "FailedLocation",
    "FileIODetails",
    "GetJobRequest",
    "Job",
    "JobExecutionInfo",
    "JobExecutionStageInfo",
    "JobMetadata",
    "ListJobsRequest",
    "ListJobsResponse",
    "PipelineDescription",
    "PubSubIODetails",
    "SdkVersion",
    "SnapshotJobRequest",
    "SpannerIODetails",
    "Step",
    "TransformSummary",
    "UpdateJobRequest",
    "JobState",
    "JobView",
    "KindType",
    "AutoscalingEvent",
    "JobMessage",
    "ListJobMessagesRequest",
    "ListJobMessagesResponse",
    "StructuredMessage",
    "JobMessageImportance",
    "GetJobExecutionDetailsRequest",
    "GetJobMetricsRequest",
    "GetStageExecutionDetailsRequest",
    "JobExecutionDetails",
    "JobMetrics",
    "MetricStructuredName",
    "MetricUpdate",
    "ProgressTimeseries",
    "StageExecutionDetails",
    "StageSummary",
    "WorkerDetails",
    "WorkItemDetails",
    "ExecutionState",
    "DeleteSnapshotRequest",
    "DeleteSnapshotResponse",
    "GetSnapshotRequest",
    "ListSnapshotsRequest",
    "ListSnapshotsResponse",
    "PubsubSnapshotMetadata",
    "Snapshot",
    "SnapshotState",
    "ComputationTopology",
    "CustomSourceLocation",
    "DataDiskAssignment",
    "KeyRangeDataDiskAssignment",
    "KeyRangeLocation",
    "MountedDataDisk",
    "PubsubLocation",
    "StateFamilyConfig",
    "StreamingApplianceSnapshotConfig",
    "StreamingComputationRanges",
    "StreamingSideInputLocation",
    "StreamingStageLocation",
    "StreamLocation",
    "TopologyConfig",
    "ContainerSpec",
    "CreateJobFromTemplateRequest",
    "DynamicTemplateLaunchParams",
    "FlexTemplateRuntimeEnvironment",
    "GetTemplateRequest",
    "GetTemplateResponse",
    "InvalidTemplateParameters",
    "LaunchFlexTemplateParameter",
    "LaunchFlexTemplateRequest",
    "LaunchFlexTemplateResponse",
    "LaunchTemplateParameters",
    "LaunchTemplateRequest",
    "LaunchTemplateResponse",
    "ParameterMetadata",
    "RuntimeEnvironment",
    "RuntimeMetadata",
    "SDKInfo",
    "TemplateMetadata",
    "ParameterType",
)
