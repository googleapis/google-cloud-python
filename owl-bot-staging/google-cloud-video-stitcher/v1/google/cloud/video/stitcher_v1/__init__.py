# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
from google.cloud.video.stitcher_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.video_stitcher_service import VideoStitcherServiceClient
from .services.video_stitcher_service import VideoStitcherServiceAsyncClient

from .types.ad_tag_details import AdRequest
from .types.ad_tag_details import LiveAdTagDetail
from .types.ad_tag_details import RequestMetadata
from .types.ad_tag_details import ResponseMetadata
from .types.ad_tag_details import VodAdTagDetail
from .types.cdn_keys import AkamaiCdnKey
from .types.cdn_keys import CdnKey
from .types.cdn_keys import GoogleCdnKey
from .types.cdn_keys import MediaCdnKey
from .types.companions import Companion
from .types.companions import CompanionAds
from .types.companions import HtmlAdResource
from .types.companions import IframeAdResource
from .types.companions import StaticAdResource
from .types.events import Event
from .types.events import ProgressEvent
from .types.fetch_options import FetchOptions
from .types.live_configs import GamLiveConfig
from .types.live_configs import LiveConfig
from .types.live_configs import PrefetchConfig
from .types.live_configs import AdTracking
from .types.sessions import Interstitials
from .types.sessions import LiveSession
from .types.sessions import ManifestOptions
from .types.sessions import RenditionFilter
from .types.sessions import VodSession
from .types.sessions import VodSessionAd
from .types.sessions import VodSessionAdBreak
from .types.sessions import VodSessionContent
from .types.slates import Slate
from .types.stitch_details import AdStitchDetail
from .types.stitch_details import VodStitchDetail
from .types.video_stitcher_service import CreateCdnKeyRequest
from .types.video_stitcher_service import CreateLiveConfigRequest
from .types.video_stitcher_service import CreateLiveSessionRequest
from .types.video_stitcher_service import CreateSlateRequest
from .types.video_stitcher_service import CreateVodConfigRequest
from .types.video_stitcher_service import CreateVodSessionRequest
from .types.video_stitcher_service import DeleteCdnKeyRequest
from .types.video_stitcher_service import DeleteLiveConfigRequest
from .types.video_stitcher_service import DeleteSlateRequest
from .types.video_stitcher_service import DeleteVodConfigRequest
from .types.video_stitcher_service import GetCdnKeyRequest
from .types.video_stitcher_service import GetLiveAdTagDetailRequest
from .types.video_stitcher_service import GetLiveConfigRequest
from .types.video_stitcher_service import GetLiveSessionRequest
from .types.video_stitcher_service import GetSlateRequest
from .types.video_stitcher_service import GetVodAdTagDetailRequest
from .types.video_stitcher_service import GetVodConfigRequest
from .types.video_stitcher_service import GetVodSessionRequest
from .types.video_stitcher_service import GetVodStitchDetailRequest
from .types.video_stitcher_service import ListCdnKeysRequest
from .types.video_stitcher_service import ListCdnKeysResponse
from .types.video_stitcher_service import ListLiveAdTagDetailsRequest
from .types.video_stitcher_service import ListLiveAdTagDetailsResponse
from .types.video_stitcher_service import ListLiveConfigsRequest
from .types.video_stitcher_service import ListLiveConfigsResponse
from .types.video_stitcher_service import ListSlatesRequest
from .types.video_stitcher_service import ListSlatesResponse
from .types.video_stitcher_service import ListVodAdTagDetailsRequest
from .types.video_stitcher_service import ListVodAdTagDetailsResponse
from .types.video_stitcher_service import ListVodConfigsRequest
from .types.video_stitcher_service import ListVodConfigsResponse
from .types.video_stitcher_service import ListVodStitchDetailsRequest
from .types.video_stitcher_service import ListVodStitchDetailsResponse
from .types.video_stitcher_service import OperationMetadata
from .types.video_stitcher_service import UpdateCdnKeyRequest
from .types.video_stitcher_service import UpdateLiveConfigRequest
from .types.video_stitcher_service import UpdateSlateRequest
from .types.video_stitcher_service import UpdateVodConfigRequest
from .types.vod_configs import GamVodConfig
from .types.vod_configs import VodConfig

__all__ = (
    'VideoStitcherServiceAsyncClient',
'AdRequest',
'AdStitchDetail',
'AdTracking',
'AkamaiCdnKey',
'CdnKey',
'Companion',
'CompanionAds',
'CreateCdnKeyRequest',
'CreateLiveConfigRequest',
'CreateLiveSessionRequest',
'CreateSlateRequest',
'CreateVodConfigRequest',
'CreateVodSessionRequest',
'DeleteCdnKeyRequest',
'DeleteLiveConfigRequest',
'DeleteSlateRequest',
'DeleteVodConfigRequest',
'Event',
'FetchOptions',
'GamLiveConfig',
'GamVodConfig',
'GetCdnKeyRequest',
'GetLiveAdTagDetailRequest',
'GetLiveConfigRequest',
'GetLiveSessionRequest',
'GetSlateRequest',
'GetVodAdTagDetailRequest',
'GetVodConfigRequest',
'GetVodSessionRequest',
'GetVodStitchDetailRequest',
'GoogleCdnKey',
'HtmlAdResource',
'IframeAdResource',
'Interstitials',
'ListCdnKeysRequest',
'ListCdnKeysResponse',
'ListLiveAdTagDetailsRequest',
'ListLiveAdTagDetailsResponse',
'ListLiveConfigsRequest',
'ListLiveConfigsResponse',
'ListSlatesRequest',
'ListSlatesResponse',
'ListVodAdTagDetailsRequest',
'ListVodAdTagDetailsResponse',
'ListVodConfigsRequest',
'ListVodConfigsResponse',
'ListVodStitchDetailsRequest',
'ListVodStitchDetailsResponse',
'LiveAdTagDetail',
'LiveConfig',
'LiveSession',
'ManifestOptions',
'MediaCdnKey',
'OperationMetadata',
'PrefetchConfig',
'ProgressEvent',
'RenditionFilter',
'RequestMetadata',
'ResponseMetadata',
'Slate',
'StaticAdResource',
'UpdateCdnKeyRequest',
'UpdateLiveConfigRequest',
'UpdateSlateRequest',
'UpdateVodConfigRequest',
'VideoStitcherServiceClient',
'VodAdTagDetail',
'VodConfig',
'VodSession',
'VodSessionAd',
'VodSessionAdBreak',
'VodSessionContent',
'VodStitchDetail',
)
