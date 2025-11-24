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
from google.cloud.logging_v2 import gapic_version as package_version

import google.api_core as api_core
import sys

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.config_service_v2 import ConfigServiceV2Client
from .services.config_service_v2 import ConfigServiceV2AsyncClient
from .services.logging_service_v2 import LoggingServiceV2Client
from .services.logging_service_v2 import LoggingServiceV2AsyncClient
from .services.metrics_service_v2 import MetricsServiceV2Client
from .services.metrics_service_v2 import MetricsServiceV2AsyncClient

from .types.log_entry import LogEntry
from .types.log_entry import LogEntryOperation
from .types.log_entry import LogEntrySourceLocation
from .types.log_entry import LogSplit
from .types.logging import DeleteLogRequest
from .types.logging import ListLogEntriesRequest
from .types.logging import ListLogEntriesResponse
from .types.logging import ListLogsRequest
from .types.logging import ListLogsResponse
from .types.logging import ListMonitoredResourceDescriptorsRequest
from .types.logging import ListMonitoredResourceDescriptorsResponse
from .types.logging import TailLogEntriesRequest
from .types.logging import TailLogEntriesResponse
from .types.logging import WriteLogEntriesPartialErrors
from .types.logging import WriteLogEntriesRequest
from .types.logging import WriteLogEntriesResponse
from .types.logging_config import BigQueryDataset
from .types.logging_config import BigQueryOptions
from .types.logging_config import BucketMetadata
from .types.logging_config import CmekSettings
from .types.logging_config import CopyLogEntriesMetadata
from .types.logging_config import CopyLogEntriesRequest
from .types.logging_config import CopyLogEntriesResponse
from .types.logging_config import CreateBucketRequest
from .types.logging_config import CreateExclusionRequest
from .types.logging_config import CreateLinkRequest
from .types.logging_config import CreateSinkRequest
from .types.logging_config import CreateViewRequest
from .types.logging_config import DeleteBucketRequest
from .types.logging_config import DeleteExclusionRequest
from .types.logging_config import DeleteLinkRequest
from .types.logging_config import DeleteSinkRequest
from .types.logging_config import DeleteViewRequest
from .types.logging_config import GetBucketRequest
from .types.logging_config import GetCmekSettingsRequest
from .types.logging_config import GetExclusionRequest
from .types.logging_config import GetLinkRequest
from .types.logging_config import GetSettingsRequest
from .types.logging_config import GetSinkRequest
from .types.logging_config import GetViewRequest
from .types.logging_config import IndexConfig
from .types.logging_config import Link
from .types.logging_config import LinkMetadata
from .types.logging_config import ListBucketsRequest
from .types.logging_config import ListBucketsResponse
from .types.logging_config import ListExclusionsRequest
from .types.logging_config import ListExclusionsResponse
from .types.logging_config import ListLinksRequest
from .types.logging_config import ListLinksResponse
from .types.logging_config import ListSinksRequest
from .types.logging_config import ListSinksResponse
from .types.logging_config import ListViewsRequest
from .types.logging_config import ListViewsResponse
from .types.logging_config import LocationMetadata
from .types.logging_config import LogBucket
from .types.logging_config import LogExclusion
from .types.logging_config import LogSink
from .types.logging_config import LogView
from .types.logging_config import Settings
from .types.logging_config import UndeleteBucketRequest
from .types.logging_config import UpdateBucketRequest
from .types.logging_config import UpdateCmekSettingsRequest
from .types.logging_config import UpdateExclusionRequest
from .types.logging_config import UpdateSettingsRequest
from .types.logging_config import UpdateSinkRequest
from .types.logging_config import UpdateViewRequest
from .types.logging_config import IndexType
from .types.logging_config import LifecycleState
from .types.logging_config import OperationState
from .types.logging_metrics import CreateLogMetricRequest
from .types.logging_metrics import DeleteLogMetricRequest
from .types.logging_metrics import GetLogMetricRequest
from .types.logging_metrics import ListLogMetricsRequest
from .types.logging_metrics import ListLogMetricsResponse
from .types.logging_metrics import LogMetric
from .types.logging_metrics import UpdateLogMetricRequest

if hasattr(api_core, "check_python_version") and hasattr(api_core, "check_dependency_versions"):   # pragma: NO COVER
    api_core.check_python_version("google.cloud.logging_v2") # type: ignore
    api_core.check_dependency_versions("google.cloud.logging_v2") # type: ignore
else:   # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import warnings
        import sys

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.logging_v2"
        if sys.version_info < (3, 9):
            warnings.warn("You are using a non-supported Python version " +
                          f"({_py_version_str}).  Google will not post any further " +
                          f"updates to {_package_label} supporting this Python version. " +
                          "Please upgrade to the latest Python version, or at " +
                          f"least to Python 3.9, and then update {_package_label}.",
                          FutureWarning)
        if sys.version_info[:2] == (3, 9):
            warnings.warn(f"You are using a Python version ({_py_version_str}) " +
                          f"which Google will stop supporting in {_package_label} in " +
                          "January 2026. Please " +
                          "upgrade to the latest Python version, or at " +
                          "least to Python 3.10, before then, and " +
                          f"then update {_package_label}.",
                          FutureWarning)

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
            warnings.warn(f"Package {_package_label} depends on " +
                          f"{_dependency_package}, currently installed at version " +
                          f"{_version_used_string}. Future updates to " +
                          f"{_package_label} will require {_dependency_package} at " +
                          f"version {_next_supported_version} or higher{_recommendation}." +
                          " Please ensure " +
                          "that either (a) your Python environment doesn't pin the " +
                          f"version of {_dependency_package}, so that updates to " +
                          f"{_package_label} can require the higher version, or " +
                          "(b) you manually update your Python environment to use at " +
                          f"least version {_next_supported_version} of " +
                          f"{_dependency_package}.",
                          FutureWarning)
    except Exception:
            warnings.warn("Could not determine the version of Python " +
                          "currently being used. To continue receiving " +
                          "updates for {_package_label}, ensure you are " +
                          "using a supported version of Python; see " +
                          "https://devguide.python.org/versions/")

__all__ = (
    'ConfigServiceV2AsyncClient',
    'LoggingServiceV2AsyncClient',
    'MetricsServiceV2AsyncClient',
'BigQueryDataset',
'BigQueryOptions',
'BucketMetadata',
'CmekSettings',
'ConfigServiceV2Client',
'CopyLogEntriesMetadata',
'CopyLogEntriesRequest',
'CopyLogEntriesResponse',
'CreateBucketRequest',
'CreateExclusionRequest',
'CreateLinkRequest',
'CreateLogMetricRequest',
'CreateSinkRequest',
'CreateViewRequest',
'DeleteBucketRequest',
'DeleteExclusionRequest',
'DeleteLinkRequest',
'DeleteLogMetricRequest',
'DeleteLogRequest',
'DeleteSinkRequest',
'DeleteViewRequest',
'GetBucketRequest',
'GetCmekSettingsRequest',
'GetExclusionRequest',
'GetLinkRequest',
'GetLogMetricRequest',
'GetSettingsRequest',
'GetSinkRequest',
'GetViewRequest',
'IndexConfig',
'IndexType',
'LifecycleState',
'Link',
'LinkMetadata',
'ListBucketsRequest',
'ListBucketsResponse',
'ListExclusionsRequest',
'ListExclusionsResponse',
'ListLinksRequest',
'ListLinksResponse',
'ListLogEntriesRequest',
'ListLogEntriesResponse',
'ListLogMetricsRequest',
'ListLogMetricsResponse',
'ListLogsRequest',
'ListLogsResponse',
'ListMonitoredResourceDescriptorsRequest',
'ListMonitoredResourceDescriptorsResponse',
'ListSinksRequest',
'ListSinksResponse',
'ListViewsRequest',
'ListViewsResponse',
'LocationMetadata',
'LogBucket',
'LogEntry',
'LogEntryOperation',
'LogEntrySourceLocation',
'LogExclusion',
'LogMetric',
'LogSink',
'LogSplit',
'LogView',
'LoggingServiceV2Client',
'MetricsServiceV2Client',
'OperationState',
'Settings',
'TailLogEntriesRequest',
'TailLogEntriesResponse',
'UndeleteBucketRequest',
'UpdateBucketRequest',
'UpdateCmekSettingsRequest',
'UpdateExclusionRequest',
'UpdateLogMetricRequest',
'UpdateSettingsRequest',
'UpdateSinkRequest',
'UpdateViewRequest',
'WriteLogEntriesPartialErrors',
'WriteLogEntriesRequest',
'WriteLogEntriesResponse',
)
