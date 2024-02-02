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


from .services.livestream_service import LivestreamServiceClient
from .services.livestream_service import LivestreamServiceAsyncClient

from .types.outputs import AudioStream
from .types.outputs import ElementaryStream
from .types.outputs import Manifest
from .types.outputs import MuxStream
from .types.outputs import PreprocessingConfig
from .types.outputs import SegmentSettings
from .types.outputs import SpriteSheet
from .types.outputs import TextStream
from .types.outputs import TimecodeConfig
from .types.outputs import VideoStream
from .types.resources import Asset
from .types.resources import AudioFormat
from .types.resources import AudioStreamProperty
from .types.resources import Channel
from .types.resources import Encryption
from .types.resources import Event
from .types.resources import Input
from .types.resources import InputAttachment
from .types.resources import InputConfig
from .types.resources import InputStreamProperty
from .types.resources import LogConfig
from .types.resources import Pool
from .types.resources import VideoFormat
from .types.resources import VideoStreamProperty
from .types.service import ChannelOperationResponse
from .types.service import CreateAssetRequest
from .types.service import CreateChannelRequest
from .types.service import CreateEventRequest
from .types.service import CreateInputRequest
from .types.service import DeleteAssetRequest
from .types.service import DeleteChannelRequest
from .types.service import DeleteEventRequest
from .types.service import DeleteInputRequest
from .types.service import GetAssetRequest
from .types.service import GetChannelRequest
from .types.service import GetEventRequest
from .types.service import GetInputRequest
from .types.service import GetPoolRequest
from .types.service import ListAssetsRequest
from .types.service import ListAssetsResponse
from .types.service import ListChannelsRequest
from .types.service import ListChannelsResponse
from .types.service import ListEventsRequest
from .types.service import ListEventsResponse
from .types.service import ListInputsRequest
from .types.service import ListInputsResponse
from .types.service import OperationMetadata
from .types.service import StartChannelRequest
from .types.service import StopChannelRequest
from .types.service import UpdateChannelRequest
from .types.service import UpdateInputRequest
from .types.service import UpdatePoolRequest

__all__ = (
    'LivestreamServiceAsyncClient',
'Asset',
'AudioFormat',
'AudioStream',
'AudioStreamProperty',
'Channel',
'ChannelOperationResponse',
'CreateAssetRequest',
'CreateChannelRequest',
'CreateEventRequest',
'CreateInputRequest',
'DeleteAssetRequest',
'DeleteChannelRequest',
'DeleteEventRequest',
'DeleteInputRequest',
'ElementaryStream',
'Encryption',
'Event',
'GetAssetRequest',
'GetChannelRequest',
'GetEventRequest',
'GetInputRequest',
'GetPoolRequest',
'Input',
'InputAttachment',
'InputConfig',
'InputStreamProperty',
'ListAssetsRequest',
'ListAssetsResponse',
'ListChannelsRequest',
'ListChannelsResponse',
'ListEventsRequest',
'ListEventsResponse',
'ListInputsRequest',
'ListInputsResponse',
'LivestreamServiceClient',
'LogConfig',
'Manifest',
'MuxStream',
'OperationMetadata',
'Pool',
'PreprocessingConfig',
'SegmentSettings',
'SpriteSheet',
'StartChannelRequest',
'StopChannelRequest',
'TextStream',
'TimecodeConfig',
'UpdateChannelRequest',
'UpdateInputRequest',
'UpdatePoolRequest',
'VideoFormat',
'VideoStream',
'VideoStreamProperty',
)
