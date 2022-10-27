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
from .ad_tag_details import (
    AdRequest,
    LiveAdTagDetail,
    RequestMetadata,
    ResponseMetadata,
    VodAdTagDetail,
)
from .cdn_keys import AkamaiCdnKey, CdnKey, GoogleCdnKey, MediaCdnKey
from .companions import (
    Companion,
    CompanionAds,
    HtmlAdResource,
    IframeAdResource,
    StaticAdResource,
)
from .events import Event, ProgressEvent
from .sessions import (
    AdTag,
    Interstitials,
    LiveSession,
    ManifestOptions,
    RenditionFilter,
    VodSession,
    VodSessionAd,
    VodSessionAdBreak,
    VodSessionContent,
)
from .slates import Slate
from .stitch_details import AdStitchDetail, VodStitchDetail
from .video_stitcher_service import (
    CreateCdnKeyRequest,
    CreateLiveSessionRequest,
    CreateSlateRequest,
    CreateVodSessionRequest,
    DeleteCdnKeyRequest,
    DeleteSlateRequest,
    GetCdnKeyRequest,
    GetLiveAdTagDetailRequest,
    GetLiveSessionRequest,
    GetSlateRequest,
    GetVodAdTagDetailRequest,
    GetVodSessionRequest,
    GetVodStitchDetailRequest,
    ListCdnKeysRequest,
    ListCdnKeysResponse,
    ListLiveAdTagDetailsRequest,
    ListLiveAdTagDetailsResponse,
    ListSlatesRequest,
    ListSlatesResponse,
    ListVodAdTagDetailsRequest,
    ListVodAdTagDetailsResponse,
    ListVodStitchDetailsRequest,
    ListVodStitchDetailsResponse,
    UpdateCdnKeyRequest,
    UpdateSlateRequest,
)

__all__ = (
    "AdRequest",
    "LiveAdTagDetail",
    "RequestMetadata",
    "ResponseMetadata",
    "VodAdTagDetail",
    "AkamaiCdnKey",
    "CdnKey",
    "GoogleCdnKey",
    "MediaCdnKey",
    "Companion",
    "CompanionAds",
    "HtmlAdResource",
    "IframeAdResource",
    "StaticAdResource",
    "Event",
    "ProgressEvent",
    "AdTag",
    "Interstitials",
    "LiveSession",
    "ManifestOptions",
    "RenditionFilter",
    "VodSession",
    "VodSessionAd",
    "VodSessionAdBreak",
    "VodSessionContent",
    "Slate",
    "AdStitchDetail",
    "VodStitchDetail",
    "CreateCdnKeyRequest",
    "CreateLiveSessionRequest",
    "CreateSlateRequest",
    "CreateVodSessionRequest",
    "DeleteCdnKeyRequest",
    "DeleteSlateRequest",
    "GetCdnKeyRequest",
    "GetLiveAdTagDetailRequest",
    "GetLiveSessionRequest",
    "GetSlateRequest",
    "GetVodAdTagDetailRequest",
    "GetVodSessionRequest",
    "GetVodStitchDetailRequest",
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
    "UpdateCdnKeyRequest",
    "UpdateSlateRequest",
)
