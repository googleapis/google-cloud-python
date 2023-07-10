# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.recommender_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.recommender import RecommenderAsyncClient, RecommenderClient
from .types.insight import Insight, InsightStateInfo
from .types.insight_type_config import InsightTypeConfig, InsightTypeGenerationConfig
from .types.recommendation import (
    CostProjection,
    Impact,
    Operation,
    OperationGroup,
    Recommendation,
    RecommendationContent,
    RecommendationStateInfo,
    SecurityProjection,
    ValueMatcher,
)
from .types.recommender_config import RecommenderConfig, RecommenderGenerationConfig
from .types.recommender_service import (
    GetInsightRequest,
    GetInsightTypeConfigRequest,
    GetRecommendationRequest,
    GetRecommenderConfigRequest,
    ListInsightsRequest,
    ListInsightsResponse,
    ListRecommendationsRequest,
    ListRecommendationsResponse,
    MarkInsightAcceptedRequest,
    MarkRecommendationClaimedRequest,
    MarkRecommendationFailedRequest,
    MarkRecommendationSucceededRequest,
    UpdateInsightTypeConfigRequest,
    UpdateRecommenderConfigRequest,
)

__all__ = (
    "RecommenderAsyncClient",
    "CostProjection",
    "GetInsightRequest",
    "GetInsightTypeConfigRequest",
    "GetRecommendationRequest",
    "GetRecommenderConfigRequest",
    "Impact",
    "Insight",
    "InsightStateInfo",
    "InsightTypeConfig",
    "InsightTypeGenerationConfig",
    "ListInsightsRequest",
    "ListInsightsResponse",
    "ListRecommendationsRequest",
    "ListRecommendationsResponse",
    "MarkInsightAcceptedRequest",
    "MarkRecommendationClaimedRequest",
    "MarkRecommendationFailedRequest",
    "MarkRecommendationSucceededRequest",
    "Operation",
    "OperationGroup",
    "Recommendation",
    "RecommendationContent",
    "RecommendationStateInfo",
    "RecommenderClient",
    "RecommenderConfig",
    "RecommenderGenerationConfig",
    "SecurityProjection",
    "UpdateInsightTypeConfigRequest",
    "UpdateRecommenderConfigRequest",
    "ValueMatcher",
)
