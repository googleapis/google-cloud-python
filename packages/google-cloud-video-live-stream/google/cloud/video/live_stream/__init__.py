# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.video.live_stream import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.video.live_stream_v1.services.livestream_service.async_client import (
    LivestreamServiceAsyncClient,
)
from google.cloud.video.live_stream_v1.services.livestream_service.client import (
    LivestreamServiceClient,
)
from google.cloud.video.live_stream_v1.types.outputs import (
    AudioStream,
    ElementaryStream,
    Manifest,
    MuxStream,
    PreprocessingConfig,
    SegmentSettings,
    SpriteSheet,
    TextStream,
    TimecodeConfig,
    VideoStream,
)
from google.cloud.video.live_stream_v1.types.resources import (
    Asset,
    AudioFormat,
    AudioStreamProperty,
    Channel,
    Clip,
    Encryption,
    Event,
    Input,
    InputAttachment,
    InputConfig,
    InputStreamProperty,
    LogConfig,
    NormalizedCoordinate,
    NormalizedResolution,
    Pool,
    RetentionConfig,
    StaticOverlay,
    VideoFormat,
    VideoStreamProperty,
)
from google.cloud.video.live_stream_v1.types.service import (
    ChannelOperationResponse,
    CreateAssetRequest,
    CreateChannelRequest,
    CreateClipRequest,
    CreateEventRequest,
    CreateInputRequest,
    DeleteAssetRequest,
    DeleteChannelRequest,
    DeleteClipRequest,
    DeleteEventRequest,
    DeleteInputRequest,
    GetAssetRequest,
    GetChannelRequest,
    GetClipRequest,
    GetEventRequest,
    GetInputRequest,
    GetPoolRequest,
    ListAssetsRequest,
    ListAssetsResponse,
    ListChannelsRequest,
    ListChannelsResponse,
    ListClipsRequest,
    ListClipsResponse,
    ListEventsRequest,
    ListEventsResponse,
    ListInputsRequest,
    ListInputsResponse,
    OperationMetadata,
    StartChannelRequest,
    StopChannelRequest,
    UpdateChannelRequest,
    UpdateInputRequest,
    UpdatePoolRequest,
)

__all__ = (
    "LivestreamServiceClient",
    "LivestreamServiceAsyncClient",
    "AudioStream",
    "ElementaryStream",
    "Manifest",
    "MuxStream",
    "PreprocessingConfig",
    "SegmentSettings",
    "SpriteSheet",
    "TextStream",
    "TimecodeConfig",
    "VideoStream",
    "Asset",
    "AudioFormat",
    "AudioStreamProperty",
    "Channel",
    "Clip",
    "Encryption",
    "Event",
    "Input",
    "InputAttachment",
    "InputConfig",
    "InputStreamProperty",
    "LogConfig",
    "NormalizedCoordinate",
    "NormalizedResolution",
    "Pool",
    "RetentionConfig",
    "StaticOverlay",
    "VideoFormat",
    "VideoStreamProperty",
    "ChannelOperationResponse",
    "CreateAssetRequest",
    "CreateChannelRequest",
    "CreateClipRequest",
    "CreateEventRequest",
    "CreateInputRequest",
    "DeleteAssetRequest",
    "DeleteChannelRequest",
    "DeleteClipRequest",
    "DeleteEventRequest",
    "DeleteInputRequest",
    "GetAssetRequest",
    "GetChannelRequest",
    "GetClipRequest",
    "GetEventRequest",
    "GetInputRequest",
    "GetPoolRequest",
    "ListAssetsRequest",
    "ListAssetsResponse",
    "ListChannelsRequest",
    "ListChannelsResponse",
    "ListClipsRequest",
    "ListClipsResponse",
    "ListEventsRequest",
    "ListEventsResponse",
    "ListInputsRequest",
    "ListInputsResponse",
    "OperationMetadata",
    "StartChannelRequest",
    "StopChannelRequest",
    "UpdateChannelRequest",
    "UpdateInputRequest",
    "UpdatePoolRequest",
)
