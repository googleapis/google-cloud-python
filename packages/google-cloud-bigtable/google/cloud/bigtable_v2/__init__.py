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
from google.cloud.bigtable_v2 import gapic_version as package_version

import google.api_core as api_core
import sys

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.bigtable import BigtableClient
from .services.bigtable import BigtableAsyncClient

from .types.bigtable import CheckAndMutateRowRequest
from .types.bigtable import CheckAndMutateRowResponse
from .types.bigtable import ExecuteQueryRequest
from .types.bigtable import ExecuteQueryResponse
from .types.bigtable import GenerateInitialChangeStreamPartitionsRequest
from .types.bigtable import GenerateInitialChangeStreamPartitionsResponse
from .types.bigtable import MutateRowRequest
from .types.bigtable import MutateRowResponse
from .types.bigtable import MutateRowsRequest
from .types.bigtable import MutateRowsResponse
from .types.bigtable import PingAndWarmRequest
from .types.bigtable import PingAndWarmResponse
from .types.bigtable import PrepareQueryRequest
from .types.bigtable import PrepareQueryResponse
from .types.bigtable import RateLimitInfo
from .types.bigtable import ReadChangeStreamRequest
from .types.bigtable import ReadChangeStreamResponse
from .types.bigtable import ReadModifyWriteRowRequest
from .types.bigtable import ReadModifyWriteRowResponse
from .types.bigtable import ReadRowsRequest
from .types.bigtable import ReadRowsResponse
from .types.bigtable import SampleRowKeysRequest
from .types.bigtable import SampleRowKeysResponse
from .types.data import ArrayValue
from .types.data import Cell
from .types.data import Column
from .types.data import ColumnMetadata
from .types.data import ColumnRange
from .types.data import Family
from .types.data import Idempotency
from .types.data import Mutation
from .types.data import PartialResultSet
from .types.data import ProtoFormat
from .types.data import ProtoRows
from .types.data import ProtoRowsBatch
from .types.data import ProtoSchema
from .types.data import ReadModifyWriteRule
from .types.data import ResultSetMetadata
from .types.data import Row
from .types.data import RowFilter
from .types.data import RowRange
from .types.data import RowSet
from .types.data import StreamContinuationToken
from .types.data import StreamContinuationTokens
from .types.data import StreamPartition
from .types.data import TimestampRange
from .types.data import Value
from .types.data import ValueRange
from .types.feature_flags import FeatureFlags
from .types.peer_info import PeerInfo
from .types.request_stats import FullReadStatsView
from .types.request_stats import ReadIterationStats
from .types.request_stats import RequestLatencyStats
from .types.request_stats import RequestStats
from .types.response_params import ResponseParams
from .types.types import Type

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.bigtable_v2")  # type: ignore
    api_core.check_dependency_versions("google.cloud.bigtable_v2")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import warnings
        import sys

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.bigtable_v2"
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
    "BigtableAsyncClient",
    "ArrayValue",
    "BigtableClient",
    "Cell",
    "CheckAndMutateRowRequest",
    "CheckAndMutateRowResponse",
    "Column",
    "ColumnMetadata",
    "ColumnRange",
    "ExecuteQueryRequest",
    "ExecuteQueryResponse",
    "Family",
    "FeatureFlags",
    "FullReadStatsView",
    "GenerateInitialChangeStreamPartitionsRequest",
    "GenerateInitialChangeStreamPartitionsResponse",
    "Idempotency",
    "MutateRowRequest",
    "MutateRowResponse",
    "MutateRowsRequest",
    "MutateRowsResponse",
    "Mutation",
    "PartialResultSet",
    "PeerInfo",
    "PingAndWarmRequest",
    "PingAndWarmResponse",
    "PrepareQueryRequest",
    "PrepareQueryResponse",
    "ProtoFormat",
    "ProtoRows",
    "ProtoRowsBatch",
    "ProtoSchema",
    "RateLimitInfo",
    "ReadChangeStreamRequest",
    "ReadChangeStreamResponse",
    "ReadIterationStats",
    "ReadModifyWriteRowRequest",
    "ReadModifyWriteRowResponse",
    "ReadModifyWriteRule",
    "ReadRowsRequest",
    "ReadRowsResponse",
    "RequestLatencyStats",
    "RequestStats",
    "ResponseParams",
    "ResultSetMetadata",
    "Row",
    "RowFilter",
    "RowRange",
    "RowSet",
    "SampleRowKeysRequest",
    "SampleRowKeysResponse",
    "StreamContinuationToken",
    "StreamContinuationTokens",
    "StreamPartition",
    "TimestampRange",
    "Type",
    "Value",
    "ValueRange",
)
