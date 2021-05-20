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

from .types.asset_service import CreateFeedRequest
from .types.asset_service import DeleteFeedRequest
from .types.asset_service import Feed
from .types.asset_service import FeedOutputConfig
from .types.asset_service import GcsDestination
from .types.asset_service import GetFeedRequest
from .types.asset_service import ListFeedsRequest
from .types.asset_service import ListFeedsResponse
from .types.asset_service import OutputConfig
from .types.asset_service import PubsubDestination
from .types.asset_service import UpdateFeedRequest
from .types.asset_service import ContentType
from .types.assets import Asset
from .types.assets import Resource
from .types.assets import TemporalAsset
from .types.assets import TimeWindow

__all__ = (
    "AssetServiceAsyncClient",
    "Asset",
    "AssetServiceClient",
    "ContentType",
    "CreateFeedRequest",
    "DeleteFeedRequest",
    "Feed",
    "FeedOutputConfig",
    "GcsDestination",
    "GetFeedRequest",
    "ListFeedsRequest",
    "ListFeedsResponse",
    "OutputConfig",
    "PubsubDestination",
    "Resource",
    "TemporalAsset",
    "TimeWindow",
    "UpdateFeedRequest",
)
