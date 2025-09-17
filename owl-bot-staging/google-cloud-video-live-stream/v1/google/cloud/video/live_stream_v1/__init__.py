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
from google.cloud.video.live_stream_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.livestream_service import LivestreamServiceClient
from .services.livestream_service import LivestreamServiceAsyncClient

from .types.outputs import AudioStream
from .types.outputs import Distribution
from .types.outputs import DistributionStream
from .types.outputs import ElementaryStream
from .types.outputs import Manifest
from .types.outputs import MuxStream
from .types.outputs import PreprocessingConfig
from .types.outputs import RtmpPushOutputEndpoint
from .types.outputs import SegmentSettings
from .types.outputs import SpriteSheet
from .types.outputs import SrtPushOutputEndpoint
from .types.outputs import TextStream
from .types.outputs import TimecodeConfig
from .types.outputs import VideoStream
from .types.resources import Asset
from .types.resources import AudioFormat
from .types.resources import AudioStreamProperty
from .types.resources import AutoTranscriptionConfig
from .types.resources import Channel
from .types.resources import Clip
from .types.resources import DvrSession
from .types.resources import Encryption
from .types.resources import EncryptionUpdate
from .types.resources import Event
from .types.resources import Input
from .types.resources import InputAttachment
from .types.resources import InputConfig
from .types.resources import InputStreamProperty
from .types.resources import LogConfig
from .types.resources import NormalizedCoordinate
from .types.resources import NormalizedResolution
from .types.resources import Pool
from .types.resources import RetentionConfig
from .types.resources import StaticOverlay
from .types.resources import TimeInterval
from .types.resources import VideoFormat
from .types.resources import VideoStreamProperty
from .types.service import ChannelOperationResponse
from .types.service import CreateAssetRequest
from .types.service import CreateChannelRequest
from .types.service import CreateClipRequest
from .types.service import CreateDvrSessionRequest
from .types.service import CreateEventRequest
from .types.service import CreateInputRequest
from .types.service import DeleteAssetRequest
from .types.service import DeleteChannelRequest
from .types.service import DeleteClipRequest
from .types.service import DeleteDvrSessionRequest
from .types.service import DeleteEventRequest
from .types.service import DeleteInputRequest
from .types.service import GetAssetRequest
from .types.service import GetChannelRequest
from .types.service import GetClipRequest
from .types.service import GetDvrSessionRequest
from .types.service import GetEventRequest
from .types.service import GetInputRequest
from .types.service import GetPoolRequest
from .types.service import ListAssetsRequest
from .types.service import ListAssetsResponse
from .types.service import ListChannelsRequest
from .types.service import ListChannelsResponse
from .types.service import ListClipsRequest
from .types.service import ListClipsResponse
from .types.service import ListDvrSessionsRequest
from .types.service import ListDvrSessionsResponse
from .types.service import ListEventsRequest
from .types.service import ListEventsResponse
from .types.service import ListInputsRequest
from .types.service import ListInputsResponse
from .types.service import OperationMetadata
from .types.service import PreviewInputRequest
from .types.service import PreviewInputResponse
from .types.service import StartChannelRequest
from .types.service import StartDistributionRequest
from .types.service import StopChannelRequest
from .types.service import StopDistributionRequest
from .types.service import UpdateChannelRequest
from .types.service import UpdateDvrSessionRequest
from .types.service import UpdateInputRequest
from .types.service import UpdatePoolRequest

__all__ = (
    'LivestreamServiceAsyncClient',
'Asset',
'AudioFormat',
'AudioStream',
'AudioStreamProperty',
'AutoTranscriptionConfig',
'Channel',
'ChannelOperationResponse',
'Clip',
'CreateAssetRequest',
'CreateChannelRequest',
'CreateClipRequest',
'CreateDvrSessionRequest',
'CreateEventRequest',
'CreateInputRequest',
'DeleteAssetRequest',
'DeleteChannelRequest',
'DeleteClipRequest',
'DeleteDvrSessionRequest',
'DeleteEventRequest',
'DeleteInputRequest',
'Distribution',
'DistributionStream',
'DvrSession',
'ElementaryStream',
'Encryption',
'EncryptionUpdate',
'Event',
'GetAssetRequest',
'GetChannelRequest',
'GetClipRequest',
'GetDvrSessionRequest',
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
'ListClipsRequest',
'ListClipsResponse',
'ListDvrSessionsRequest',
'ListDvrSessionsResponse',
'ListEventsRequest',
'ListEventsResponse',
'ListInputsRequest',
'ListInputsResponse',
'LivestreamServiceClient',
'LogConfig',
'Manifest',
'MuxStream',
'NormalizedCoordinate',
'NormalizedResolution',
'OperationMetadata',
'Pool',
'PreprocessingConfig',
'PreviewInputRequest',
'PreviewInputResponse',
'RetentionConfig',
'RtmpPushOutputEndpoint',
'SegmentSettings',
'SpriteSheet',
'SrtPushOutputEndpoint',
'StartChannelRequest',
'StartDistributionRequest',
'StaticOverlay',
'StopChannelRequest',
'StopDistributionRequest',
'TextStream',
'TimeInterval',
'TimecodeConfig',
'UpdateChannelRequest',
'UpdateDvrSessionRequest',
'UpdateInputRequest',
'UpdatePoolRequest',
'VideoFormat',
'VideoStream',
'VideoStreamProperty',
)
