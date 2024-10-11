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
from google.cloud.video.stitcher import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.video.stitcher_v1.services.video_stitcher_service.client import VideoStitcherServiceClient
from google.cloud.video.stitcher_v1.services.video_stitcher_service.async_client import VideoStitcherServiceAsyncClient

from google.cloud.video.stitcher_v1.types.ad_tag_details import AdRequest
from google.cloud.video.stitcher_v1.types.ad_tag_details import LiveAdTagDetail
from google.cloud.video.stitcher_v1.types.ad_tag_details import RequestMetadata
from google.cloud.video.stitcher_v1.types.ad_tag_details import ResponseMetadata
from google.cloud.video.stitcher_v1.types.ad_tag_details import VodAdTagDetail
from google.cloud.video.stitcher_v1.types.cdn_keys import AkamaiCdnKey
from google.cloud.video.stitcher_v1.types.cdn_keys import CdnKey
from google.cloud.video.stitcher_v1.types.cdn_keys import GoogleCdnKey
from google.cloud.video.stitcher_v1.types.cdn_keys import MediaCdnKey
from google.cloud.video.stitcher_v1.types.companions import Companion
from google.cloud.video.stitcher_v1.types.companions import CompanionAds
from google.cloud.video.stitcher_v1.types.companions import HtmlAdResource
from google.cloud.video.stitcher_v1.types.companions import IframeAdResource
from google.cloud.video.stitcher_v1.types.companions import StaticAdResource
from google.cloud.video.stitcher_v1.types.events import Event
from google.cloud.video.stitcher_v1.types.events import ProgressEvent
from google.cloud.video.stitcher_v1.types.fetch_options import FetchOptions
from google.cloud.video.stitcher_v1.types.live_configs import GamLiveConfig
from google.cloud.video.stitcher_v1.types.live_configs import LiveConfig
from google.cloud.video.stitcher_v1.types.live_configs import PrefetchConfig
from google.cloud.video.stitcher_v1.types.live_configs import AdTracking
from google.cloud.video.stitcher_v1.types.sessions import Interstitials
from google.cloud.video.stitcher_v1.types.sessions import LiveSession
from google.cloud.video.stitcher_v1.types.sessions import ManifestOptions
from google.cloud.video.stitcher_v1.types.sessions import RenditionFilter
from google.cloud.video.stitcher_v1.types.sessions import VodSession
from google.cloud.video.stitcher_v1.types.sessions import VodSessionAd
from google.cloud.video.stitcher_v1.types.sessions import VodSessionAdBreak
from google.cloud.video.stitcher_v1.types.sessions import VodSessionContent
from google.cloud.video.stitcher_v1.types.slates import Slate
from google.cloud.video.stitcher_v1.types.stitch_details import AdStitchDetail
from google.cloud.video.stitcher_v1.types.stitch_details import VodStitchDetail
from google.cloud.video.stitcher_v1.types.video_stitcher_service import CreateCdnKeyRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import CreateLiveConfigRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import CreateLiveSessionRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import CreateSlateRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import CreateVodConfigRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import CreateVodSessionRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import DeleteCdnKeyRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import DeleteLiveConfigRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import DeleteSlateRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import DeleteVodConfigRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import GetCdnKeyRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import GetLiveAdTagDetailRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import GetLiveConfigRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import GetLiveSessionRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import GetSlateRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import GetVodAdTagDetailRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import GetVodConfigRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import GetVodSessionRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import GetVodStitchDetailRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListCdnKeysRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListCdnKeysResponse
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListLiveAdTagDetailsRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListLiveAdTagDetailsResponse
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListLiveConfigsRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListLiveConfigsResponse
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListSlatesRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListSlatesResponse
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListVodAdTagDetailsRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListVodAdTagDetailsResponse
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListVodConfigsRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListVodConfigsResponse
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListVodStitchDetailsRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import ListVodStitchDetailsResponse
from google.cloud.video.stitcher_v1.types.video_stitcher_service import OperationMetadata
from google.cloud.video.stitcher_v1.types.video_stitcher_service import UpdateCdnKeyRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import UpdateLiveConfigRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import UpdateSlateRequest
from google.cloud.video.stitcher_v1.types.video_stitcher_service import UpdateVodConfigRequest
from google.cloud.video.stitcher_v1.types.vod_configs import GamVodConfig
from google.cloud.video.stitcher_v1.types.vod_configs import VodConfig

__all__ = ('VideoStitcherServiceClient',
    'VideoStitcherServiceAsyncClient',
    'AdRequest',
    'LiveAdTagDetail',
    'RequestMetadata',
    'ResponseMetadata',
    'VodAdTagDetail',
    'AkamaiCdnKey',
    'CdnKey',
    'GoogleCdnKey',
    'MediaCdnKey',
    'Companion',
    'CompanionAds',
    'HtmlAdResource',
    'IframeAdResource',
    'StaticAdResource',
    'Event',
    'ProgressEvent',
    'FetchOptions',
    'GamLiveConfig',
    'LiveConfig',
    'PrefetchConfig',
    'AdTracking',
    'Interstitials',
    'LiveSession',
    'ManifestOptions',
    'RenditionFilter',
    'VodSession',
    'VodSessionAd',
    'VodSessionAdBreak',
    'VodSessionContent',
    'Slate',
    'AdStitchDetail',
    'VodStitchDetail',
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
    'GetCdnKeyRequest',
    'GetLiveAdTagDetailRequest',
    'GetLiveConfigRequest',
    'GetLiveSessionRequest',
    'GetSlateRequest',
    'GetVodAdTagDetailRequest',
    'GetVodConfigRequest',
    'GetVodSessionRequest',
    'GetVodStitchDetailRequest',
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
    'OperationMetadata',
    'UpdateCdnKeyRequest',
    'UpdateLiveConfigRequest',
    'UpdateSlateRequest',
    'UpdateVodConfigRequest',
    'GamVodConfig',
    'VodConfig',
)
