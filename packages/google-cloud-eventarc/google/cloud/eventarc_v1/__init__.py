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
from google.cloud.eventarc_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.eventarc import EventarcAsyncClient, EventarcClient
from .types.channel import Channel
from .types.channel_connection import ChannelConnection
from .types.discovery import EventType, FilteringAttribute, Provider
from .types.eventarc import (
    CreateChannelConnectionRequest,
    CreateChannelRequest,
    CreateTriggerRequest,
    DeleteChannelConnectionRequest,
    DeleteChannelRequest,
    DeleteTriggerRequest,
    GetChannelConnectionRequest,
    GetChannelRequest,
    GetGoogleChannelConfigRequest,
    GetProviderRequest,
    GetTriggerRequest,
    ListChannelConnectionsRequest,
    ListChannelConnectionsResponse,
    ListChannelsRequest,
    ListChannelsResponse,
    ListProvidersRequest,
    ListProvidersResponse,
    ListTriggersRequest,
    ListTriggersResponse,
    OperationMetadata,
    UpdateChannelRequest,
    UpdateGoogleChannelConfigRequest,
    UpdateTriggerRequest,
)
from .types.google_channel_config import GoogleChannelConfig
from .types.trigger import (
    GKE,
    CloudRun,
    Destination,
    EventFilter,
    Pubsub,
    StateCondition,
    Transport,
    Trigger,
)

__all__ = (
    "EventarcAsyncClient",
    "Channel",
    "ChannelConnection",
    "CloudRun",
    "CreateChannelConnectionRequest",
    "CreateChannelRequest",
    "CreateTriggerRequest",
    "DeleteChannelConnectionRequest",
    "DeleteChannelRequest",
    "DeleteTriggerRequest",
    "Destination",
    "EventFilter",
    "EventType",
    "EventarcClient",
    "FilteringAttribute",
    "GKE",
    "GetChannelConnectionRequest",
    "GetChannelRequest",
    "GetGoogleChannelConfigRequest",
    "GetProviderRequest",
    "GetTriggerRequest",
    "GoogleChannelConfig",
    "ListChannelConnectionsRequest",
    "ListChannelConnectionsResponse",
    "ListChannelsRequest",
    "ListChannelsResponse",
    "ListProvidersRequest",
    "ListProvidersResponse",
    "ListTriggersRequest",
    "ListTriggersResponse",
    "OperationMetadata",
    "Provider",
    "Pubsub",
    "StateCondition",
    "Transport",
    "Trigger",
    "UpdateChannelRequest",
    "UpdateGoogleChannelConfigRequest",
    "UpdateTriggerRequest",
)
