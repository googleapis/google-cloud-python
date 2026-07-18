# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
from google.showcase import gapic_version as package_version

__version__ = package_version.__version__


from google.showcase_v1beta1.services.echo.client import EchoClient
from google.showcase_v1beta1.services.echo.async_client import EchoAsyncClient
from google.showcase_v1beta1.services.identity.client import IdentityClient
from google.showcase_v1beta1.services.identity.async_client import IdentityAsyncClient
from google.showcase_v1beta1.services.messaging.client import MessagingClient
from google.showcase_v1beta1.services.messaging.async_client import MessagingAsyncClient

from google.showcase_v1beta1.types.echo import BlockRequest
from google.showcase_v1beta1.types.echo import BlockResponse
from google.showcase_v1beta1.types.echo import EchoErrorDetailsRequest
from google.showcase_v1beta1.types.echo import EchoErrorDetailsResponse
from google.showcase_v1beta1.types.echo import EchoRequest
from google.showcase_v1beta1.types.echo import EchoResponse
from google.showcase_v1beta1.types.echo import ErrorWithMultipleDetails
from google.showcase_v1beta1.types.echo import ErrorWithSingleDetail
from google.showcase_v1beta1.types.echo import ExpandRequest
from google.showcase_v1beta1.types.echo import PagedExpandLegacyMappedResponse
from google.showcase_v1beta1.types.echo import PagedExpandLegacyRequest
from google.showcase_v1beta1.types.echo import PagedExpandRequest
from google.showcase_v1beta1.types.echo import PagedExpandResponse
from google.showcase_v1beta1.types.echo import PagedExpandResponseList
from google.showcase_v1beta1.types.echo import WaitMetadata
from google.showcase_v1beta1.types.echo import WaitRequest
from google.showcase_v1beta1.types.echo import WaitResponse
from google.showcase_v1beta1.types.echo import Severity
from google.showcase_v1beta1.types.identity import CreateUserRequest
from google.showcase_v1beta1.types.identity import DeleteUserRequest
from google.showcase_v1beta1.types.identity import GetUserRequest
from google.showcase_v1beta1.types.identity import ListUsersRequest
from google.showcase_v1beta1.types.identity import ListUsersResponse
from google.showcase_v1beta1.types.identity import UpdateUserRequest
from google.showcase_v1beta1.types.identity import User
from google.showcase_v1beta1.types.messaging import Blurb
from google.showcase_v1beta1.types.messaging import ConnectRequest
from google.showcase_v1beta1.types.messaging import CreateBlurbRequest
from google.showcase_v1beta1.types.messaging import CreateRoomRequest
from google.showcase_v1beta1.types.messaging import DeleteBlurbRequest
from google.showcase_v1beta1.types.messaging import DeleteRoomRequest
from google.showcase_v1beta1.types.messaging import GetBlurbRequest
from google.showcase_v1beta1.types.messaging import GetRoomRequest
from google.showcase_v1beta1.types.messaging import ListBlurbsRequest
from google.showcase_v1beta1.types.messaging import ListBlurbsResponse
from google.showcase_v1beta1.types.messaging import ListRoomsRequest
from google.showcase_v1beta1.types.messaging import ListRoomsResponse
from google.showcase_v1beta1.types.messaging import Room
from google.showcase_v1beta1.types.messaging import SearchBlurbsMetadata
from google.showcase_v1beta1.types.messaging import SearchBlurbsRequest
from google.showcase_v1beta1.types.messaging import SearchBlurbsResponse
from google.showcase_v1beta1.types.messaging import SendBlurbsResponse
from google.showcase_v1beta1.types.messaging import StreamBlurbsRequest
from google.showcase_v1beta1.types.messaging import StreamBlurbsResponse
from google.showcase_v1beta1.types.messaging import UpdateBlurbRequest
from google.showcase_v1beta1.types.messaging import UpdateRoomRequest

__all__ = ('EchoClient',
    'EchoAsyncClient',
    'IdentityClient',
    'IdentityAsyncClient',
    'MessagingClient',
    'MessagingAsyncClient',
    'BlockRequest',
    'BlockResponse',
    'EchoErrorDetailsRequest',
    'EchoErrorDetailsResponse',
    'EchoRequest',
    'EchoResponse',
    'ErrorWithMultipleDetails',
    'ErrorWithSingleDetail',
    'ExpandRequest',
    'PagedExpandLegacyMappedResponse',
    'PagedExpandLegacyRequest',
    'PagedExpandRequest',
    'PagedExpandResponse',
    'PagedExpandResponseList',
    'WaitMetadata',
    'WaitRequest',
    'WaitResponse',
    'Severity',
    'CreateUserRequest',
    'DeleteUserRequest',
    'GetUserRequest',
    'ListUsersRequest',
    'ListUsersResponse',
    'UpdateUserRequest',
    'User',
    'Blurb',
    'ConnectRequest',
    'CreateBlurbRequest',
    'CreateRoomRequest',
    'DeleteBlurbRequest',
    'DeleteRoomRequest',
    'GetBlurbRequest',
    'GetRoomRequest',
    'ListBlurbsRequest',
    'ListBlurbsResponse',
    'ListRoomsRequest',
    'ListRoomsResponse',
    'Room',
    'SearchBlurbsMetadata',
    'SearchBlurbsRequest',
    'SearchBlurbsResponse',
    'SendBlurbsResponse',
    'StreamBlurbsRequest',
    'StreamBlurbsResponse',
    'UpdateBlurbRequest',
    'UpdateRoomRequest',
)
