# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from .services.asset_service import AssetServiceClient
from .services.asset_service import AssetServiceAsyncClient

from .types.asset_service import AnalyzeIamPolicyLongrunningMetadata
from .types.asset_service import AnalyzeIamPolicyLongrunningRequest
from .types.asset_service import AnalyzeIamPolicyLongrunningResponse
from .types.asset_service import AnalyzeIamPolicyRequest
from .types.asset_service import AnalyzeIamPolicyResponse
from .types.asset_service import AnalyzeMoveRequest
from .types.asset_service import AnalyzeMoveResponse
from .types.asset_service import BatchGetAssetsHistoryRequest
from .types.asset_service import BatchGetAssetsHistoryResponse
from .types.asset_service import BigQueryDestination
from .types.asset_service import CreateFeedRequest
from .types.asset_service import DeleteFeedRequest
from .types.asset_service import ExportAssetsRequest
from .types.asset_service import ExportAssetsResponse
from .types.asset_service import Feed
from .types.asset_service import FeedOutputConfig
from .types.asset_service import GcsDestination
from .types.asset_service import GcsOutputResult
from .types.asset_service import GetFeedRequest
from .types.asset_service import IamPolicyAnalysisOutputConfig
from .types.asset_service import IamPolicyAnalysisQuery
from .types.asset_service import ListAssetsRequest
from .types.asset_service import ListAssetsResponse
from .types.asset_service import ListFeedsRequest
from .types.asset_service import ListFeedsResponse
from .types.asset_service import MoveAnalysis
from .types.asset_service import MoveAnalysisResult
from .types.asset_service import MoveImpact
from .types.asset_service import OutputConfig
from .types.asset_service import OutputResult
from .types.asset_service import PartitionSpec
from .types.asset_service import PubsubDestination
from .types.asset_service import SearchAllIamPoliciesRequest
from .types.asset_service import SearchAllIamPoliciesResponse
from .types.asset_service import SearchAllResourcesRequest
from .types.asset_service import SearchAllResourcesResponse
from .types.asset_service import UpdateFeedRequest
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

__all__ = (
    "AssetServiceAsyncClient",
    "AnalyzeIamPolicyLongrunningMetadata",
    "AnalyzeIamPolicyLongrunningRequest",
    "AnalyzeIamPolicyLongrunningResponse",
    "AnalyzeIamPolicyRequest",
    "AnalyzeIamPolicyResponse",
    "AnalyzeMoveRequest",
    "AnalyzeMoveResponse",
    "Asset",
    "AssetServiceClient",
    "AttachedResource",
    "BatchGetAssetsHistoryRequest",
    "BatchGetAssetsHistoryResponse",
    "BigQueryDestination",
    "ConditionEvaluation",
    "ContentType",
    "CreateFeedRequest",
    "DeleteFeedRequest",
    "ExportAssetsRequest",
    "ExportAssetsResponse",
    "Feed",
    "FeedOutputConfig",
    "GcsDestination",
    "GcsOutputResult",
    "GetFeedRequest",
    "IamPolicyAnalysisOutputConfig",
    "IamPolicyAnalysisQuery",
    "IamPolicyAnalysisResult",
    "IamPolicyAnalysisState",
    "IamPolicySearchResult",
    "ListAssetsRequest",
    "ListAssetsResponse",
    "ListFeedsRequest",
    "ListFeedsResponse",
    "MoveAnalysis",
    "MoveAnalysisResult",
    "MoveImpact",
    "OutputConfig",
    "OutputResult",
    "PartitionSpec",
    "PubsubDestination",
    "RelatedAsset",
    "RelatedAssets",
    "RelatedResource",
    "RelatedResources",
    "RelationshipAttributes",
    "Resource",
    "ResourceSearchResult",
    "SearchAllIamPoliciesRequest",
    "SearchAllIamPoliciesResponse",
    "SearchAllResourcesRequest",
    "SearchAllResourcesResponse",
    "TemporalAsset",
    "TimeWindow",
    "UpdateFeedRequest",
    "VersionedResource",
)
