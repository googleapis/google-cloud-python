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
from google.cloud.logging import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.logging_v2.services.config_service_v2.async_client import (
    ConfigServiceV2AsyncClient,
)
from google.cloud.logging_v2.services.config_service_v2.client import (
    ConfigServiceV2Client,
)
from google.cloud.logging_v2.services.logging_service_v2.async_client import (
    LoggingServiceV2AsyncClient,
)
from google.cloud.logging_v2.services.logging_service_v2.client import (
    LoggingServiceV2Client,
)
from google.cloud.logging_v2.services.metrics_service_v2.async_client import (
    MetricsServiceV2AsyncClient,
)
from google.cloud.logging_v2.services.metrics_service_v2.client import (
    MetricsServiceV2Client,
)
from google.cloud.logging_v2.types.log_entry import (
    LogEntry,
    LogEntryOperation,
    LogEntrySourceLocation,
    LogSplit,
)
from google.cloud.logging_v2.types.logging import (
    DeleteLogRequest,
    ListLogEntriesRequest,
    ListLogEntriesResponse,
    ListLogsRequest,
    ListLogsResponse,
    ListMonitoredResourceDescriptorsRequest,
    ListMonitoredResourceDescriptorsResponse,
    TailLogEntriesRequest,
    TailLogEntriesResponse,
    WriteLogEntriesPartialErrors,
    WriteLogEntriesRequest,
    WriteLogEntriesResponse,
)
from google.cloud.logging_v2.types.logging_config import (
    BigQueryDataset,
    BigQueryOptions,
    BucketMetadata,
    CmekSettings,
    CopyLogEntriesMetadata,
    CopyLogEntriesRequest,
    CopyLogEntriesResponse,
    CreateBucketRequest,
    CreateExclusionRequest,
    CreateLinkRequest,
    CreateSinkRequest,
    CreateViewRequest,
    DeleteBucketRequest,
    DeleteExclusionRequest,
    DeleteLinkRequest,
    DeleteSinkRequest,
    DeleteViewRequest,
    GetBucketRequest,
    GetCmekSettingsRequest,
    GetExclusionRequest,
    GetLinkRequest,
    GetSettingsRequest,
    GetSinkRequest,
    GetViewRequest,
    IndexConfig,
    IndexType,
    LifecycleState,
    Link,
    LinkMetadata,
    ListBucketsRequest,
    ListBucketsResponse,
    ListExclusionsRequest,
    ListExclusionsResponse,
    ListLinksRequest,
    ListLinksResponse,
    ListSinksRequest,
    ListSinksResponse,
    ListViewsRequest,
    ListViewsResponse,
    LocationMetadata,
    LogBucket,
    LogExclusion,
    LogSink,
    LogView,
    OperationState,
    Settings,
    UndeleteBucketRequest,
    UpdateBucketRequest,
    UpdateCmekSettingsRequest,
    UpdateExclusionRequest,
    UpdateSettingsRequest,
    UpdateSinkRequest,
    UpdateViewRequest,
)
from google.cloud.logging_v2.types.logging_metrics import (
    CreateLogMetricRequest,
    DeleteLogMetricRequest,
    GetLogMetricRequest,
    ListLogMetricsRequest,
    ListLogMetricsResponse,
    LogMetric,
    UpdateLogMetricRequest,
)

__all__ = (
    "ConfigServiceV2Client",
    "ConfigServiceV2AsyncClient",
    "LoggingServiceV2Client",
    "LoggingServiceV2AsyncClient",
    "MetricsServiceV2Client",
    "MetricsServiceV2AsyncClient",
    "LogEntry",
    "LogEntryOperation",
    "LogEntrySourceLocation",
    "LogSplit",
    "DeleteLogRequest",
    "ListLogEntriesRequest",
    "ListLogEntriesResponse",
    "ListLogsRequest",
    "ListLogsResponse",
    "ListMonitoredResourceDescriptorsRequest",
    "ListMonitoredResourceDescriptorsResponse",
    "TailLogEntriesRequest",
    "TailLogEntriesResponse",
    "WriteLogEntriesPartialErrors",
    "WriteLogEntriesRequest",
    "WriteLogEntriesResponse",
    "BigQueryDataset",
    "BigQueryOptions",
    "BucketMetadata",
    "CmekSettings",
    "CopyLogEntriesMetadata",
    "CopyLogEntriesRequest",
    "CopyLogEntriesResponse",
    "CreateBucketRequest",
    "CreateExclusionRequest",
    "CreateLinkRequest",
    "CreateSinkRequest",
    "CreateViewRequest",
    "DeleteBucketRequest",
    "DeleteExclusionRequest",
    "DeleteLinkRequest",
    "DeleteSinkRequest",
    "DeleteViewRequest",
    "GetBucketRequest",
    "GetCmekSettingsRequest",
    "GetExclusionRequest",
    "GetLinkRequest",
    "GetSettingsRequest",
    "GetSinkRequest",
    "GetViewRequest",
    "IndexConfig",
    "Link",
    "LinkMetadata",
    "ListBucketsRequest",
    "ListBucketsResponse",
    "ListExclusionsRequest",
    "ListExclusionsResponse",
    "ListLinksRequest",
    "ListLinksResponse",
    "ListSinksRequest",
    "ListSinksResponse",
    "ListViewsRequest",
    "ListViewsResponse",
    "LocationMetadata",
    "LogBucket",
    "LogExclusion",
    "LogSink",
    "LogView",
    "Settings",
    "UndeleteBucketRequest",
    "UpdateBucketRequest",
    "UpdateCmekSettingsRequest",
    "UpdateExclusionRequest",
    "UpdateSettingsRequest",
    "UpdateSinkRequest",
    "UpdateViewRequest",
    "IndexType",
    "LifecycleState",
    "OperationState",
    "CreateLogMetricRequest",
    "DeleteLogMetricRequest",
    "GetLogMetricRequest",
    "ListLogMetricsRequest",
    "ListLogMetricsResponse",
    "LogMetric",
    "UpdateLogMetricRequest",
)
