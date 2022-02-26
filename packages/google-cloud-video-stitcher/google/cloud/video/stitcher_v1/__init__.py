# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from .types.companions import Companion
from .types.companions import CompanionAds
from .types.companions import HtmlAdResource
from .types.companions import IframeAdResource
from .types.companions import StaticAdResource
from .types.events import Event
from .types.events import ProgressEvent
from .types.sessions import AdTag
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
from .types.video_stitcher_service import CreateLiveSessionRequest
from .types.video_stitcher_service import CreateSlateRequest
from .types.video_stitcher_service import CreateVodSessionRequest
from .types.video_stitcher_service import DeleteCdnKeyRequest
from .types.video_stitcher_service import DeleteSlateRequest
from .types.video_stitcher_service import GetCdnKeyRequest
from .types.video_stitcher_service import GetLiveAdTagDetailRequest
from .types.video_stitcher_service import GetLiveSessionRequest
from .types.video_stitcher_service import GetSlateRequest
from .types.video_stitcher_service import GetVodAdTagDetailRequest
from .types.video_stitcher_service import GetVodSessionRequest
from .types.video_stitcher_service import GetVodStitchDetailRequest
from .types.video_stitcher_service import ListCdnKeysRequest
from .types.video_stitcher_service import ListCdnKeysResponse
from .types.video_stitcher_service import ListLiveAdTagDetailsRequest
from .types.video_stitcher_service import ListLiveAdTagDetailsResponse
from .types.video_stitcher_service import ListSlatesRequest
from .types.video_stitcher_service import ListSlatesResponse
from .types.video_stitcher_service import ListVodAdTagDetailsRequest
from .types.video_stitcher_service import ListVodAdTagDetailsResponse
from .types.video_stitcher_service import ListVodStitchDetailsRequest
from .types.video_stitcher_service import ListVodStitchDetailsResponse
from .types.video_stitcher_service import UpdateCdnKeyRequest
from .types.video_stitcher_service import UpdateSlateRequest

__all__ = (
    "VideoStitcherServiceAsyncClient",
    "AdRequest",
    "AdStitchDetail",
    "AdTag",
    "AkamaiCdnKey",
    "CdnKey",
    "Companion",
    "CompanionAds",
    "CreateCdnKeyRequest",
    "CreateLiveSessionRequest",
    "CreateSlateRequest",
    "CreateVodSessionRequest",
    "DeleteCdnKeyRequest",
    "DeleteSlateRequest",
    "Event",
    "GetCdnKeyRequest",
    "GetLiveAdTagDetailRequest",
    "GetLiveSessionRequest",
    "GetSlateRequest",
    "GetVodAdTagDetailRequest",
    "GetVodSessionRequest",
    "GetVodStitchDetailRequest",
    "GoogleCdnKey",
    "HtmlAdResource",
    "IframeAdResource",
    "Interstitials",
    "ListCdnKeysRequest",
    "ListCdnKeysResponse",
    "ListLiveAdTagDetailsRequest",
    "ListLiveAdTagDetailsResponse",
    "ListSlatesRequest",
    "ListSlatesResponse",
    "ListVodAdTagDetailsRequest",
    "ListVodAdTagDetailsResponse",
    "ListVodStitchDetailsRequest",
    "ListVodStitchDetailsResponse",
    "LiveAdTagDetail",
    "LiveSession",
    "ManifestOptions",
    "ProgressEvent",
    "RenditionFilter",
    "RequestMetadata",
    "ResponseMetadata",
    "Slate",
    "StaticAdResource",
    "UpdateCdnKeyRequest",
    "UpdateSlateRequest",
    "VideoStitcherServiceClient",
    "VodAdTagDetail",
    "VodSession",
    "VodSessionAd",
    "VodSessionAdBreak",
    "VodSessionContent",
    "VodStitchDetail",
)
