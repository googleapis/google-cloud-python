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
from google.cloud.video.live_stream_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.livestream_service import (
    LivestreamServiceAsyncClient,
    LivestreamServiceClient,
)
from .types.outputs import (
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
from .types.resources import (
    AudioFormat,
    AudioStreamProperty,
    Channel,
    Encryption,
    Event,
    Input,
    InputAttachment,
    InputConfig,
    InputStreamProperty,
    LogConfig,
    VideoFormat,
    VideoStreamProperty,
)
from .types.service import (
    ChannelOperationResponse,
    CreateChannelRequest,
    CreateEventRequest,
    CreateInputRequest,
    DeleteChannelRequest,
    DeleteEventRequest,
    DeleteInputRequest,
    GetChannelRequest,
    GetEventRequest,
    GetInputRequest,
    ListChannelsRequest,
    ListChannelsResponse,
    ListEventsRequest,
    ListEventsResponse,
    ListInputsRequest,
    ListInputsResponse,
    OperationMetadata,
    StartChannelRequest,
    StopChannelRequest,
    UpdateChannelRequest,
    UpdateInputRequest,
)

__all__ = (
    "LivestreamServiceAsyncClient",
    "AudioFormat",
    "AudioStream",
    "AudioStreamProperty",
    "Channel",
    "ChannelOperationResponse",
    "CreateChannelRequest",
    "CreateEventRequest",
    "CreateInputRequest",
    "DeleteChannelRequest",
    "DeleteEventRequest",
    "DeleteInputRequest",
    "ElementaryStream",
    "Encryption",
    "Event",
    "GetChannelRequest",
    "GetEventRequest",
    "GetInputRequest",
    "Input",
    "InputAttachment",
    "InputConfig",
    "InputStreamProperty",
    "ListChannelsRequest",
    "ListChannelsResponse",
    "ListEventsRequest",
    "ListEventsResponse",
    "ListInputsRequest",
    "ListInputsResponse",
    "LivestreamServiceClient",
    "LogConfig",
    "Manifest",
    "MuxStream",
    "OperationMetadata",
    "PreprocessingConfig",
    "SegmentSettings",
    "SpriteSheet",
    "StartChannelRequest",
    "StopChannelRequest",
    "TextStream",
    "TimecodeConfig",
    "UpdateChannelRequest",
    "UpdateInputRequest",
    "VideoFormat",
    "VideoStream",
    "VideoStreamProperty",
)
