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
from google.cloud.video.stitcher import gapic_version as package_version

__version__ = package_version.__version__


from .services.video_stitcher_service import (
    VideoStitcherServiceAsyncClient,
    VideoStitcherServiceClient,
)
from .types.ad_tag_details import (
    AdRequest,
    LiveAdTagDetail,
    RequestMetadata,
    ResponseMetadata,
    VodAdTagDetail,
)
from .types.cdn_keys import AkamaiCdnKey, CdnKey, GoogleCdnKey, MediaCdnKey
from .types.companions import (
    Companion,
    CompanionAds,
    HtmlAdResource,
    IframeAdResource,
    StaticAdResource,
)
from .types.events import Event, ProgressEvent
from .types.sessions import (
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
from .types.slates import Slate
from .types.stitch_details import AdStitchDetail, VodStitchDetail
from .types.video_stitcher_service import (
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
    "MediaCdnKey",
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
