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
from google.cloud.asset import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.asset_v1p2beta1.services.asset_service.client import AssetServiceClient
from google.cloud.asset_v1p2beta1.services.asset_service.async_client import AssetServiceAsyncClient

from google.cloud.asset_v1p2beta1.types.asset_service import CreateFeedRequest
from google.cloud.asset_v1p2beta1.types.asset_service import DeleteFeedRequest
from google.cloud.asset_v1p2beta1.types.asset_service import Feed
from google.cloud.asset_v1p2beta1.types.asset_service import FeedOutputConfig
from google.cloud.asset_v1p2beta1.types.asset_service import GcsDestination
from google.cloud.asset_v1p2beta1.types.asset_service import GetFeedRequest
from google.cloud.asset_v1p2beta1.types.asset_service import ListFeedsRequest
from google.cloud.asset_v1p2beta1.types.asset_service import ListFeedsResponse
from google.cloud.asset_v1p2beta1.types.asset_service import OutputConfig
from google.cloud.asset_v1p2beta1.types.asset_service import PubsubDestination
from google.cloud.asset_v1p2beta1.types.asset_service import UpdateFeedRequest
from google.cloud.asset_v1p2beta1.types.asset_service import ContentType
from google.cloud.asset_v1p2beta1.types.assets import Asset
from google.cloud.asset_v1p2beta1.types.assets import Resource
from google.cloud.asset_v1p2beta1.types.assets import TemporalAsset
from google.cloud.asset_v1p2beta1.types.assets import TimeWindow

__all__ = ('AssetServiceClient',
    'AssetServiceAsyncClient',
    'CreateFeedRequest',
    'DeleteFeedRequest',
    'Feed',
    'FeedOutputConfig',
    'GcsDestination',
    'GetFeedRequest',
    'ListFeedsRequest',
    'ListFeedsResponse',
    'OutputConfig',
    'PubsubDestination',
    'UpdateFeedRequest',
    'ContentType',
    'Asset',
    'Resource',
    'TemporalAsset',
    'TimeWindow',
)
