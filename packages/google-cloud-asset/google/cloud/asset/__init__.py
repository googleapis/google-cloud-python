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

from google.cloud.asset_v1.services.asset_service.client import AssetServiceClient
from google.cloud.asset_v1.services.asset_service.async_client import (
    AssetServiceAsyncClient,
)

from google.cloud.asset_v1.types.asset_service import AnalyzeIamPolicyLongrunningRequest
from google.cloud.asset_v1.types.asset_service import (
    AnalyzeIamPolicyLongrunningResponse,
)
from google.cloud.asset_v1.types.asset_service import AnalyzeIamPolicyRequest
from google.cloud.asset_v1.types.asset_service import AnalyzeIamPolicyResponse
from google.cloud.asset_v1.types.asset_service import BatchGetAssetsHistoryRequest
from google.cloud.asset_v1.types.asset_service import BatchGetAssetsHistoryResponse
from google.cloud.asset_v1.types.asset_service import BigQueryDestination
from google.cloud.asset_v1.types.asset_service import CreateFeedRequest
from google.cloud.asset_v1.types.asset_service import DeleteFeedRequest
from google.cloud.asset_v1.types.asset_service import ExportAssetsRequest
from google.cloud.asset_v1.types.asset_service import ExportAssetsResponse
from google.cloud.asset_v1.types.asset_service import Feed
from google.cloud.asset_v1.types.asset_service import FeedOutputConfig
from google.cloud.asset_v1.types.asset_service import GcsDestination
from google.cloud.asset_v1.types.asset_service import GcsOutputResult
from google.cloud.asset_v1.types.asset_service import GetFeedRequest
from google.cloud.asset_v1.types.asset_service import IamPolicyAnalysisOutputConfig
from google.cloud.asset_v1.types.asset_service import IamPolicyAnalysisQuery
from google.cloud.asset_v1.types.asset_service import ListAssetsRequest
from google.cloud.asset_v1.types.asset_service import ListAssetsResponse
from google.cloud.asset_v1.types.asset_service import ListFeedsRequest
from google.cloud.asset_v1.types.asset_service import ListFeedsResponse
from google.cloud.asset_v1.types.asset_service import OutputConfig
from google.cloud.asset_v1.types.asset_service import OutputResult
from google.cloud.asset_v1.types.asset_service import PartitionSpec
from google.cloud.asset_v1.types.asset_service import PubsubDestination
from google.cloud.asset_v1.types.asset_service import SearchAllIamPoliciesRequest
from google.cloud.asset_v1.types.asset_service import SearchAllIamPoliciesResponse
from google.cloud.asset_v1.types.asset_service import SearchAllResourcesRequest
from google.cloud.asset_v1.types.asset_service import SearchAllResourcesResponse
from google.cloud.asset_v1.types.asset_service import UpdateFeedRequest
from google.cloud.asset_v1.types.asset_service import ContentType
from google.cloud.asset_v1.types.assets import Asset
from google.cloud.asset_v1.types.assets import ConditionEvaluation
from google.cloud.asset_v1.types.assets import IamPolicyAnalysisResult
from google.cloud.asset_v1.types.assets import IamPolicyAnalysisState
from google.cloud.asset_v1.types.assets import IamPolicySearchResult
from google.cloud.asset_v1.types.assets import Resource
from google.cloud.asset_v1.types.assets import ResourceSearchResult
from google.cloud.asset_v1.types.assets import TemporalAsset
from google.cloud.asset_v1.types.assets import TimeWindow

__all__ = (
    "AssetServiceClient",
    "AssetServiceAsyncClient",
    "AnalyzeIamPolicyLongrunningRequest",
    "AnalyzeIamPolicyLongrunningResponse",
    "AnalyzeIamPolicyRequest",
    "AnalyzeIamPolicyResponse",
    "BatchGetAssetsHistoryRequest",
    "BatchGetAssetsHistoryResponse",
    "BigQueryDestination",
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
    "ListAssetsRequest",
    "ListAssetsResponse",
    "ListFeedsRequest",
    "ListFeedsResponse",
    "OutputConfig",
    "OutputResult",
    "PartitionSpec",
    "PubsubDestination",
    "SearchAllIamPoliciesRequest",
    "SearchAllIamPoliciesResponse",
    "SearchAllResourcesRequest",
    "SearchAllResourcesResponse",
    "UpdateFeedRequest",
    "ContentType",
    "Asset",
    "ConditionEvaluation",
    "IamPolicyAnalysisResult",
    "IamPolicyAnalysisState",
    "IamPolicySearchResult",
    "Resource",
    "ResourceSearchResult",
    "TemporalAsset",
    "TimeWindow",
)
