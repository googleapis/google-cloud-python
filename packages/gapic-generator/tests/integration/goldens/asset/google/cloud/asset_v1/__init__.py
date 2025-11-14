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
from google.cloud.asset_v1 import gapic_version as package_version

import google.api_core as api_core
import sys

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.asset_service import AssetServiceClient
from .services.asset_service import AssetServiceAsyncClient

from .types.asset_service import AnalyzeIamPolicyLongrunningMetadata
from .types.asset_service import AnalyzeIamPolicyLongrunningRequest
from .types.asset_service import AnalyzeIamPolicyLongrunningResponse
from .types.asset_service import AnalyzeIamPolicyRequest
from .types.asset_service import AnalyzeIamPolicyResponse
from .types.asset_service import AnalyzeMoveRequest
from .types.asset_service import AnalyzeMoveResponse
from .types.asset_service import AnalyzeOrgPoliciesRequest
from .types.asset_service import AnalyzeOrgPoliciesResponse
from .types.asset_service import AnalyzeOrgPolicyGovernedAssetsRequest
from .types.asset_service import AnalyzeOrgPolicyGovernedAssetsResponse
from .types.asset_service import AnalyzeOrgPolicyGovernedContainersRequest
from .types.asset_service import AnalyzeOrgPolicyGovernedContainersResponse
from .types.asset_service import AnalyzerOrgPolicy
from .types.asset_service import AnalyzerOrgPolicyConstraint
from .types.asset_service import BatchGetAssetsHistoryRequest
from .types.asset_service import BatchGetAssetsHistoryResponse
from .types.asset_service import BatchGetEffectiveIamPoliciesRequest
from .types.asset_service import BatchGetEffectiveIamPoliciesResponse
from .types.asset_service import BigQueryDestination
from .types.asset_service import CreateFeedRequest
from .types.asset_service import CreateSavedQueryRequest
from .types.asset_service import DeleteFeedRequest
from .types.asset_service import DeleteSavedQueryRequest
from .types.asset_service import ExportAssetsRequest
from .types.asset_service import ExportAssetsResponse
from .types.asset_service import Feed
from .types.asset_service import FeedOutputConfig
from .types.asset_service import GcsDestination
from .types.asset_service import GcsOutputResult
from .types.asset_service import GetFeedRequest
from .types.asset_service import GetSavedQueryRequest
from .types.asset_service import IamPolicyAnalysisOutputConfig
from .types.asset_service import IamPolicyAnalysisQuery
from .types.asset_service import ListAssetsRequest
from .types.asset_service import ListAssetsResponse
from .types.asset_service import ListFeedsRequest
from .types.asset_service import ListFeedsResponse
from .types.asset_service import ListSavedQueriesRequest
from .types.asset_service import ListSavedQueriesResponse
from .types.asset_service import MoveAnalysis
from .types.asset_service import MoveAnalysisResult
from .types.asset_service import MoveImpact
from .types.asset_service import OutputConfig
from .types.asset_service import OutputResult
from .types.asset_service import PartitionSpec
from .types.asset_service import PubsubDestination
from .types.asset_service import QueryAssetsOutputConfig
from .types.asset_service import QueryAssetsRequest
from .types.asset_service import QueryAssetsResponse
from .types.asset_service import QueryResult
from .types.asset_service import SavedQuery
from .types.asset_service import SearchAllIamPoliciesRequest
from .types.asset_service import SearchAllIamPoliciesResponse
from .types.asset_service import SearchAllResourcesRequest
from .types.asset_service import SearchAllResourcesResponse
from .types.asset_service import TableFieldSchema
from .types.asset_service import TableSchema
from .types.asset_service import UpdateFeedRequest
from .types.asset_service import UpdateSavedQueryRequest
from .types.asset_service import ContentType
from .types.assets import Asset
from .types.assets import AttachedResource
from .types.assets import ConditionEvaluation
from .types.assets import IamPolicyAnalysisResult
from .types.assets import IamPolicyAnalysisState
from .types.assets import IamPolicySearchResult
from .types.assets import RelatedAsset
from .types.assets import RelatedAssets
from .types.assets import RelatedResource
from .types.assets import RelatedResources
from .types.assets import RelationshipAttributes
from .types.assets import Resource
from .types.assets import ResourceSearchResult
from .types.assets import TemporalAsset
from .types.assets import TimeWindow
from .types.assets import VersionedResource

if hasattr(api_core, "check_python_version") and hasattr(api_core, "check_dependency_versions"):   # pragma: NO COVER
    api_core.check_python_version("google.cloud.asset_v1") # type: ignore
    api_core.check_dependency_versions("google.cloud.asset_v1") # type: ignore
else:   # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import warnings
        import sys

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.asset_v1"
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
    'AssetServiceAsyncClient',
'AnalyzeIamPolicyLongrunningMetadata',
'AnalyzeIamPolicyLongrunningRequest',
'AnalyzeIamPolicyLongrunningResponse',
'AnalyzeIamPolicyRequest',
'AnalyzeIamPolicyResponse',
'AnalyzeMoveRequest',
'AnalyzeMoveResponse',
'AnalyzeOrgPoliciesRequest',
'AnalyzeOrgPoliciesResponse',
'AnalyzeOrgPolicyGovernedAssetsRequest',
'AnalyzeOrgPolicyGovernedAssetsResponse',
'AnalyzeOrgPolicyGovernedContainersRequest',
'AnalyzeOrgPolicyGovernedContainersResponse',
'AnalyzerOrgPolicy',
'AnalyzerOrgPolicyConstraint',
'Asset',
'AssetServiceClient',
'AttachedResource',
'BatchGetAssetsHistoryRequest',
'BatchGetAssetsHistoryResponse',
'BatchGetEffectiveIamPoliciesRequest',
'BatchGetEffectiveIamPoliciesResponse',
'BigQueryDestination',
'ConditionEvaluation',
'ContentType',
'CreateFeedRequest',
'CreateSavedQueryRequest',
'DeleteFeedRequest',
'DeleteSavedQueryRequest',
'ExportAssetsRequest',
'ExportAssetsResponse',
'Feed',
'FeedOutputConfig',
'GcsDestination',
'GcsOutputResult',
'GetFeedRequest',
'GetSavedQueryRequest',
'IamPolicyAnalysisOutputConfig',
'IamPolicyAnalysisQuery',
'IamPolicyAnalysisResult',
'IamPolicyAnalysisState',
'IamPolicySearchResult',
'ListAssetsRequest',
'ListAssetsResponse',
'ListFeedsRequest',
'ListFeedsResponse',
'ListSavedQueriesRequest',
'ListSavedQueriesResponse',
'MoveAnalysis',
'MoveAnalysisResult',
'MoveImpact',
'OutputConfig',
'OutputResult',
'PartitionSpec',
'PubsubDestination',
'QueryAssetsOutputConfig',
'QueryAssetsRequest',
'QueryAssetsResponse',
'QueryResult',
'RelatedAsset',
'RelatedAssets',
'RelatedResource',
'RelatedResources',
'RelationshipAttributes',
'Resource',
'ResourceSearchResult',
'SavedQuery',
'SearchAllIamPoliciesRequest',
'SearchAllIamPoliciesResponse',
'SearchAllResourcesRequest',
'SearchAllResourcesResponse',
'TableFieldSchema',
'TableSchema',
'TemporalAsset',
'TimeWindow',
'UpdateFeedRequest',
'UpdateSavedQueryRequest',
'VersionedResource',
)
