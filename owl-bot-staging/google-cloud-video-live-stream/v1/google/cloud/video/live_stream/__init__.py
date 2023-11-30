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
from google.cloud.video.live_stream import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.video.live_stream_v1.services.livestream_service.client import LivestreamServiceClient
from google.cloud.video.live_stream_v1.services.livestream_service.async_client import LivestreamServiceAsyncClient

from google.cloud.video.live_stream_v1.types.outputs import AudioStream
from google.cloud.video.live_stream_v1.types.outputs import ElementaryStream
from google.cloud.video.live_stream_v1.types.outputs import Manifest
from google.cloud.video.live_stream_v1.types.outputs import MuxStream
from google.cloud.video.live_stream_v1.types.outputs import PreprocessingConfig
from google.cloud.video.live_stream_v1.types.outputs import SegmentSettings
from google.cloud.video.live_stream_v1.types.outputs import SpriteSheet
from google.cloud.video.live_stream_v1.types.outputs import TextStream
from google.cloud.video.live_stream_v1.types.outputs import TimecodeConfig
from google.cloud.video.live_stream_v1.types.outputs import VideoStream
from google.cloud.video.live_stream_v1.types.resources import Asset
from google.cloud.video.live_stream_v1.types.resources import AudioFormat
from google.cloud.video.live_stream_v1.types.resources import AudioStreamProperty
from google.cloud.video.live_stream_v1.types.resources import Channel
from google.cloud.video.live_stream_v1.types.resources import Encryption
from google.cloud.video.live_stream_v1.types.resources import Event
from google.cloud.video.live_stream_v1.types.resources import Input
from google.cloud.video.live_stream_v1.types.resources import InputAttachment
from google.cloud.video.live_stream_v1.types.resources import InputConfig
from google.cloud.video.live_stream_v1.types.resources import InputStreamProperty
from google.cloud.video.live_stream_v1.types.resources import LogConfig
from google.cloud.video.live_stream_v1.types.resources import Pool
from google.cloud.video.live_stream_v1.types.resources import VideoFormat
from google.cloud.video.live_stream_v1.types.resources import VideoStreamProperty
from google.cloud.video.live_stream_v1.types.service import ChannelOperationResponse
from google.cloud.video.live_stream_v1.types.service import CreateAssetRequest
from google.cloud.video.live_stream_v1.types.service import CreateChannelRequest
from google.cloud.video.live_stream_v1.types.service import CreateEventRequest
from google.cloud.video.live_stream_v1.types.service import CreateInputRequest
from google.cloud.video.live_stream_v1.types.service import DeleteAssetRequest
from google.cloud.video.live_stream_v1.types.service import DeleteChannelRequest
from google.cloud.video.live_stream_v1.types.service import DeleteEventRequest
from google.cloud.video.live_stream_v1.types.service import DeleteInputRequest
from google.cloud.video.live_stream_v1.types.service import GetAssetRequest
from google.cloud.video.live_stream_v1.types.service import GetChannelRequest
from google.cloud.video.live_stream_v1.types.service import GetEventRequest
from google.cloud.video.live_stream_v1.types.service import GetInputRequest
from google.cloud.video.live_stream_v1.types.service import GetPoolRequest
from google.cloud.video.live_stream_v1.types.service import ListAssetsRequest
from google.cloud.video.live_stream_v1.types.service import ListAssetsResponse
from google.cloud.video.live_stream_v1.types.service import ListChannelsRequest
from google.cloud.video.live_stream_v1.types.service import ListChannelsResponse
from google.cloud.video.live_stream_v1.types.service import ListEventsRequest
from google.cloud.video.live_stream_v1.types.service import ListEventsResponse
from google.cloud.video.live_stream_v1.types.service import ListInputsRequest
from google.cloud.video.live_stream_v1.types.service import ListInputsResponse
from google.cloud.video.live_stream_v1.types.service import OperationMetadata
from google.cloud.video.live_stream_v1.types.service import StartChannelRequest
from google.cloud.video.live_stream_v1.types.service import StopChannelRequest
from google.cloud.video.live_stream_v1.types.service import UpdateChannelRequest
from google.cloud.video.live_stream_v1.types.service import UpdateInputRequest
from google.cloud.video.live_stream_v1.types.service import UpdatePoolRequest

__all__ = ('LivestreamServiceClient',
    'LivestreamServiceAsyncClient',
    'AudioStream',
    'ElementaryStream',
    'Manifest',
    'MuxStream',
    'PreprocessingConfig',
    'SegmentSettings',
    'SpriteSheet',
    'TextStream',
    'TimecodeConfig',
    'VideoStream',
    'Asset',
    'AudioFormat',
    'AudioStreamProperty',
    'Channel',
    'Encryption',
    'Event',
    'Input',
    'InputAttachment',
    'InputConfig',
    'InputStreamProperty',
    'LogConfig',
    'Pool',
    'VideoFormat',
    'VideoStreamProperty',
    'ChannelOperationResponse',
    'CreateAssetRequest',
    'CreateChannelRequest',
    'CreateEventRequest',
    'CreateInputRequest',
    'DeleteAssetRequest',
    'DeleteChannelRequest',
    'DeleteEventRequest',
    'DeleteInputRequest',
    'GetAssetRequest',
    'GetChannelRequest',
    'GetEventRequest',
    'GetInputRequest',
    'GetPoolRequest',
    'ListAssetsRequest',
    'ListAssetsResponse',
    'ListChannelsRequest',
    'ListChannelsResponse',
    'ListEventsRequest',
    'ListEventsResponse',
    'ListInputsRequest',
    'ListInputsResponse',
    'OperationMetadata',
    'StartChannelRequest',
    'StopChannelRequest',
    'UpdateChannelRequest',
    'UpdateInputRequest',
    'UpdatePoolRequest',
)
