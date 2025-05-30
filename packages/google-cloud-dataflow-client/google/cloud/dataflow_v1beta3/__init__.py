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
from google.cloud.dataflow_v1beta3 import gapic_version as package_version

__version__ = package_version.__version__


from .services.flex_templates_service import (
    FlexTemplatesServiceAsyncClient,
    FlexTemplatesServiceClient,
)
from .services.jobs_v1_beta3 import JobsV1Beta3AsyncClient, JobsV1Beta3Client
from .services.messages_v1_beta3 import (
    MessagesV1Beta3AsyncClient,
    MessagesV1Beta3Client,
)
from .services.metrics_v1_beta3 import MetricsV1Beta3AsyncClient, MetricsV1Beta3Client
from .services.snapshots_v1_beta3 import (
    SnapshotsV1Beta3AsyncClient,
    SnapshotsV1Beta3Client,
)
from .services.templates_service import (
    TemplatesServiceAsyncClient,
    TemplatesServiceClient,
)
from .types.environment import (
    AutoscalingAlgorithm,
    AutoscalingSettings,
    DataSamplingConfig,
    DebugOptions,
    DefaultPackageSet,
    Disk,
    Environment,
    FlexResourceSchedulingGoal,
    JobType,
    Package,
    SdkHarnessContainerImage,
    ShuffleMode,
    StreamingMode,
    TaskRunnerSettings,
    TeardownPolicy,
    WorkerIPAddressConfiguration,
    WorkerPool,
    WorkerSettings,
)
from .types.jobs import (
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
    RuntimeUpdatableParams,
    SdkBug,
    SdkVersion,
    ServiceResources,
    SnapshotJobRequest,
    SpannerIODetails,
    Step,
    TransformSummary,
    UpdateJobRequest,
)
from .types.messages import (
    AutoscalingEvent,
    JobMessage,
    JobMessageImportance,
    ListJobMessagesRequest,
    ListJobMessagesResponse,
    StructuredMessage,
)
from .types.metrics import (
    ExecutionState,
    GetJobExecutionDetailsRequest,
    GetJobMetricsRequest,
    GetStageExecutionDetailsRequest,
    HotKeyDebuggingInfo,
    JobExecutionDetails,
    JobMetrics,
    MetricStructuredName,
    MetricUpdate,
    ProgressTimeseries,
    StageExecutionDetails,
    StageSummary,
    Straggler,
    StragglerInfo,
    StragglerSummary,
    StreamingStragglerInfo,
    WorkerDetails,
    WorkItemDetails,
)
from .types.snapshots import (
    DeleteSnapshotRequest,
    DeleteSnapshotResponse,
    GetSnapshotRequest,
    ListSnapshotsRequest,
    ListSnapshotsResponse,
    PubsubSnapshotMetadata,
    Snapshot,
    SnapshotState,
)
from .types.streaming import (
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
from .types.templates import (
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
    ParameterMetadataEnumOption,
    ParameterType,
    RuntimeEnvironment,
    RuntimeMetadata,
    SDKInfo,
    TemplateMetadata,
)

__all__ = (
    "FlexTemplatesServiceAsyncClient",
    "JobsV1Beta3AsyncClient",
    "MessagesV1Beta3AsyncClient",
    "MetricsV1Beta3AsyncClient",
    "SnapshotsV1Beta3AsyncClient",
    "TemplatesServiceAsyncClient",
    "AutoscalingAlgorithm",
    "AutoscalingEvent",
    "AutoscalingSettings",
    "BigQueryIODetails",
    "BigTableIODetails",
    "CheckActiveJobsRequest",
    "CheckActiveJobsResponse",
    "ComputationTopology",
    "ContainerSpec",
    "CreateJobFromTemplateRequest",
    "CreateJobRequest",
    "CustomSourceLocation",
    "DataDiskAssignment",
    "DataSamplingConfig",
    "DatastoreIODetails",
    "DebugOptions",
    "DefaultPackageSet",
    "DeleteSnapshotRequest",
    "DeleteSnapshotResponse",
    "Disk",
    "DisplayData",
    "DynamicTemplateLaunchParams",
    "Environment",
    "ExecutionStageState",
    "ExecutionStageSummary",
    "ExecutionState",
    "FailedLocation",
    "FileIODetails",
    "FlexResourceSchedulingGoal",
    "FlexTemplateRuntimeEnvironment",
    "FlexTemplatesServiceClient",
    "GetJobExecutionDetailsRequest",
    "GetJobMetricsRequest",
    "GetJobRequest",
    "GetSnapshotRequest",
    "GetStageExecutionDetailsRequest",
    "GetTemplateRequest",
    "GetTemplateResponse",
    "HotKeyDebuggingInfo",
    "InvalidTemplateParameters",
    "Job",
    "JobExecutionDetails",
    "JobExecutionInfo",
    "JobExecutionStageInfo",
    "JobMessage",
    "JobMessageImportance",
    "JobMetadata",
    "JobMetrics",
    "JobState",
    "JobType",
    "JobView",
    "JobsV1Beta3Client",
    "KeyRangeDataDiskAssignment",
    "KeyRangeLocation",
    "KindType",
    "LaunchFlexTemplateParameter",
    "LaunchFlexTemplateRequest",
    "LaunchFlexTemplateResponse",
    "LaunchTemplateParameters",
    "LaunchTemplateRequest",
    "LaunchTemplateResponse",
    "ListJobMessagesRequest",
    "ListJobMessagesResponse",
    "ListJobsRequest",
    "ListJobsResponse",
    "ListSnapshotsRequest",
    "ListSnapshotsResponse",
    "MessagesV1Beta3Client",
    "MetricStructuredName",
    "MetricUpdate",
    "MetricsV1Beta3Client",
    "MountedDataDisk",
    "Package",
    "ParameterMetadata",
    "ParameterMetadataEnumOption",
    "ParameterType",
    "PipelineDescription",
    "ProgressTimeseries",
    "PubSubIODetails",
    "PubsubLocation",
    "PubsubSnapshotMetadata",
    "RuntimeEnvironment",
    "RuntimeMetadata",
    "RuntimeUpdatableParams",
    "SDKInfo",
    "SdkBug",
    "SdkHarnessContainerImage",
    "SdkVersion",
    "ServiceResources",
    "ShuffleMode",
    "Snapshot",
    "SnapshotJobRequest",
    "SnapshotState",
    "SnapshotsV1Beta3Client",
    "SpannerIODetails",
    "StageExecutionDetails",
    "StageSummary",
    "StateFamilyConfig",
    "Step",
    "Straggler",
    "StragglerInfo",
    "StragglerSummary",
    "StreamLocation",
    "StreamingApplianceSnapshotConfig",
    "StreamingComputationRanges",
    "StreamingMode",
    "StreamingSideInputLocation",
    "StreamingStageLocation",
    "StreamingStragglerInfo",
    "StructuredMessage",
    "TaskRunnerSettings",
    "TeardownPolicy",
    "TemplateMetadata",
    "TemplatesServiceClient",
    "TopologyConfig",
    "TransformSummary",
    "UpdateJobRequest",
    "WorkItemDetails",
    "WorkerDetails",
    "WorkerIPAddressConfiguration",
    "WorkerPool",
    "WorkerSettings",
)
