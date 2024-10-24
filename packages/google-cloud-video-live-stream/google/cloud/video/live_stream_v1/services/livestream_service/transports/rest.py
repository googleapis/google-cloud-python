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

import dataclasses
import json  # type: ignore
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, operations_v1, rest_helpers, rest_streaming
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.video.live_stream_v1.types import resources, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseLivestreamServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class LivestreamServiceRestInterceptor:
    """Interceptor for LivestreamService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the LivestreamServiceRestTransport.

    .. code-block:: python
        class MyCustomLivestreamServiceInterceptor(LivestreamServiceRestInterceptor):
            def pre_create_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_clip(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_clip(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_input(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_clip(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_clip(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_input(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_asset(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_asset(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_clip(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_clip(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_input(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_assets(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_assets(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_channels(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_channels(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_clips(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_clips(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_inputs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_inputs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_start_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_start_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_stop_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_stop_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_input(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_input(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_pool(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_pool(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = LivestreamServiceRestTransport(interceptor=MyCustomLivestreamServiceInterceptor())
        client = LivestreamServiceClient(transport=transport)


    """

    def pre_create_asset(
        self, request: service.CreateAssetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_create_asset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_asset

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_create_channel(
        self, request: service.CreateChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_create_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_create_clip(
        self, request: service.CreateClipRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateClipRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_clip

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_create_clip(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_clip

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_create_event(
        self, request: service.CreateEventRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_create_event(self, response: resources.Event) -> resources.Event:
        """Post-rpc interceptor for create_event

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_create_input(
        self, request: service.CreateInputRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.CreateInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_create_input(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_input

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_asset(
        self, request: service.DeleteAssetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_delete_asset(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_asset

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_channel(
        self, request: service.DeleteChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_delete_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_clip(
        self, request: service.DeleteClipRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteClipRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_clip

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_delete_clip(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_clip

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_event(
        self, request: service.DeleteEventRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def pre_delete_input(
        self, request: service.DeleteInputRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.DeleteInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_delete_input(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_input

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_asset(
        self, request: service.GetAssetRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetAssetRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_asset

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_asset(self, response: resources.Asset) -> resources.Asset:
        """Post-rpc interceptor for get_asset

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_channel(
        self, request: service.GetChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_channel(self, response: resources.Channel) -> resources.Channel:
        """Post-rpc interceptor for get_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_clip(
        self, request: service.GetClipRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetClipRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_clip

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_clip(self, response: resources.Clip) -> resources.Clip:
        """Post-rpc interceptor for get_clip

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_event(
        self, request: service.GetEventRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_event(self, response: resources.Event) -> resources.Event:
        """Post-rpc interceptor for get_event

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_input(
        self, request: service.GetInputRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_input(self, response: resources.Input) -> resources.Input:
        """Post-rpc interceptor for get_input

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_pool(
        self, request: service.GetPoolRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetPoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_pool(self, response: resources.Pool) -> resources.Pool:
        """Post-rpc interceptor for get_pool

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_list_assets(
        self, request: service.ListAssetsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListAssetsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_assets

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_list_assets(
        self, response: service.ListAssetsResponse
    ) -> service.ListAssetsResponse:
        """Post-rpc interceptor for list_assets

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_list_channels(
        self, request: service.ListChannelsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListChannelsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_channels

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_list_channels(
        self, response: service.ListChannelsResponse
    ) -> service.ListChannelsResponse:
        """Post-rpc interceptor for list_channels

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_list_clips(
        self, request: service.ListClipsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListClipsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_clips

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_list_clips(
        self, response: service.ListClipsResponse
    ) -> service.ListClipsResponse:
        """Post-rpc interceptor for list_clips

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_list_events(
        self, request: service.ListEventsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListEventsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_list_events(
        self, response: service.ListEventsResponse
    ) -> service.ListEventsResponse:
        """Post-rpc interceptor for list_events

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_list_inputs(
        self, request: service.ListInputsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.ListInputsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_inputs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_list_inputs(
        self, response: service.ListInputsResponse
    ) -> service.ListInputsResponse:
        """Post-rpc interceptor for list_inputs

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_start_channel(
        self, request: service.StartChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.StartChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for start_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_start_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for start_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_stop_channel(
        self, request: service.StopChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.StopChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for stop_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_stop_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for stop_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_update_channel(
        self, request: service.UpdateChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_update_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_channel

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_update_input(
        self, request: service.UpdateInputRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdateInputRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_input

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_update_input(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_input

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_update_pool(
        self, request: service.UpdatePoolRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.UpdatePoolRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_pool

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_update_pool(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_pool

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_location(
        self,
        request: locations_pb2.GetLocationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.GetLocationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_location

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_list_locations(
        self,
        request: locations_pb2.ListLocationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[locations_pb2.ListLocationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_locations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_cancel_operation(
        self,
        request: operations_pb2.CancelOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.CancelOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_operation(
        self,
        request: operations_pb2.DeleteOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.DeleteOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_get_operation(
        self,
        request: operations_pb2.GetOperationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.GetOperationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_operation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response

    def pre_list_operations(
        self,
        request: operations_pb2.ListOperationsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[operations_pb2.ListOperationsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_operations

        Override in a subclass to manipulate the request or metadata
        before they are sent to the LivestreamService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the LivestreamService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class LivestreamServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: LivestreamServiceRestInterceptor


class LivestreamServiceRestTransport(_BaseLivestreamServiceRestTransport):
    """REST backend synchronous transport for LivestreamService.

    Using Live Stream API, you can generate live streams in the
    various renditions and streaming formats. The streaming format
    include HTTP Live Streaming (HLS) and Dynamic Adaptive Streaming
    over HTTP (DASH). You can send a source stream in the various
    ways, including Real-Time Messaging Protocol (RTMP) and Secure
    Reliable Transport (SRT).

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "livestream.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[LivestreamServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'livestream.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or LivestreamServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {
                "google.longrunning.Operations.CancelOperation": [
                    {
                        "method": "post",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateAsset(
        _BaseLivestreamServiceRestTransport._BaseCreateAsset, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.CreateAsset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.CreateAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create asset method over HTTP.

            Args:
                request (~.service.CreateAssetRequest):
                    The request object. Request message for
                "LivestreamService.CreateAsset".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseCreateAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_asset(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseCreateAsset._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseCreateAsset._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseCreateAsset._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._CreateAsset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_asset(resp)
            return resp

    class _CreateChannel(
        _BaseLivestreamServiceRestTransport._BaseCreateChannel,
        LivestreamServiceRestStub,
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.CreateChannel")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.CreateChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create channel method over HTTP.

            Args:
                request (~.service.CreateChannelRequest):
                    The request object. Request message for
                "LivestreamService.CreateChannel".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseCreateChannel._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_channel(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseCreateChannel._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseCreateChannel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseCreateChannel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._CreateChannel._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_channel(resp)
            return resp

    class _CreateClip(
        _BaseLivestreamServiceRestTransport._BaseCreateClip, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.CreateClip")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.CreateClipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create clip method over HTTP.

            Args:
                request (~.service.CreateClipRequest):
                    The request object. Request message for
                "LivestreamService.CreateClip".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseCreateClip._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_clip(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseCreateClip._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseCreateClip._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseCreateClip._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._CreateClip._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_clip(resp)
            return resp

    class _CreateEvent(
        _BaseLivestreamServiceRestTransport._BaseCreateEvent, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.CreateEvent")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.CreateEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Event:
            r"""Call the create event method over HTTP.

            Args:
                request (~.service.CreateEventRequest):
                    The request object. Request message for
                "LivestreamService.CreateEvent".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Event:
                    Event is a sub-resource of a channel,
                which can be scheduled by the user to
                execute operations on a channel resource
                without having to stop the channel.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseCreateEvent._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_event(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseCreateEvent._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseCreateEvent._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseCreateEvent._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._CreateEvent._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Event()
            pb_resp = resources.Event.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_event(resp)
            return resp

    class _CreateInput(
        _BaseLivestreamServiceRestTransport._BaseCreateInput, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.CreateInput")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.CreateInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create input method over HTTP.

            Args:
                request (~.service.CreateInputRequest):
                    The request object. Request message for
                "LivestreamService.CreateInput".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseCreateInput._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_input(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseCreateInput._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseCreateInput._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseCreateInput._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._CreateInput._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_input(resp)
            return resp

    class _DeleteAsset(
        _BaseLivestreamServiceRestTransport._BaseDeleteAsset, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.DeleteAsset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.DeleteAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete asset method over HTTP.

            Args:
                request (~.service.DeleteAssetRequest):
                    The request object. Request message for
                "LivestreamService.DeleteAsset".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseDeleteAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_asset(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseDeleteAsset._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseDeleteAsset._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._DeleteAsset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_asset(resp)
            return resp

    class _DeleteChannel(
        _BaseLivestreamServiceRestTransport._BaseDeleteChannel,
        LivestreamServiceRestStub,
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.DeleteChannel")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.DeleteChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete channel method over HTTP.

            Args:
                request (~.service.DeleteChannelRequest):
                    The request object. Request message for
                "LivestreamService.DeleteChannel".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseDeleteChannel._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_channel(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseDeleteChannel._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseDeleteChannel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._DeleteChannel._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_channel(resp)
            return resp

    class _DeleteClip(
        _BaseLivestreamServiceRestTransport._BaseDeleteClip, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.DeleteClip")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.DeleteClipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete clip method over HTTP.

            Args:
                request (~.service.DeleteClipRequest):
                    The request object. Request message for
                "LivestreamService.DeleteClip".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseDeleteClip._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_clip(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseDeleteClip._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseDeleteClip._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._DeleteClip._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_clip(resp)
            return resp

    class _DeleteEvent(
        _BaseLivestreamServiceRestTransport._BaseDeleteEvent, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.DeleteEvent")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.DeleteEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete event method over HTTP.

            Args:
                request (~.service.DeleteEventRequest):
                    The request object. Request message for
                "LivestreamService.DeleteEvent".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseDeleteEvent._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_event(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseDeleteEvent._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseDeleteEvent._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._DeleteEvent._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

    class _DeleteInput(
        _BaseLivestreamServiceRestTransport._BaseDeleteInput, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.DeleteInput")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.DeleteInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete input method over HTTP.

            Args:
                request (~.service.DeleteInputRequest):
                    The request object. Request message for
                "LivestreamService.DeleteInput".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseDeleteInput._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_input(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseDeleteInput._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseDeleteInput._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._DeleteInput._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_input(resp)
            return resp

    class _GetAsset(
        _BaseLivestreamServiceRestTransport._BaseGetAsset, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.GetAsset")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetAssetRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Asset:
            r"""Call the get asset method over HTTP.

            Args:
                request (~.service.GetAssetRequest):
                    The request object. Request message for
                "LivestreamService.GetAsset".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Asset:
                    An asset represents a video or an
                image.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseGetAsset._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_asset(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseGetAsset._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseGetAsset._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._GetAsset._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Asset()
            pb_resp = resources.Asset.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_asset(resp)
            return resp

    class _GetChannel(
        _BaseLivestreamServiceRestTransport._BaseGetChannel, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.GetChannel")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Channel:
            r"""Call the get channel method over HTTP.

            Args:
                request (~.service.GetChannelRequest):
                    The request object. Request message for
                "LivestreamService.GetChannel".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Channel:
                    Channel resource represents the
                processor that does a user-defined
                "streaming" operation, which includes
                getting an input stream through an
                input, transcoding it to multiple
                renditions, and publishing output live
                streams in certain formats (for example,
                HLS or DASH) to the specified location.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseGetChannel._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_channel(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseGetChannel._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseGetChannel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._GetChannel._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Channel()
            pb_resp = resources.Channel.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_channel(resp)
            return resp

    class _GetClip(
        _BaseLivestreamServiceRestTransport._BaseGetClip, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.GetClip")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetClipRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Clip:
            r"""Call the get clip method over HTTP.

            Args:
                request (~.service.GetClipRequest):
                    The request object. Request message for
                "LivestreamService.GetClip".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Clip:
                    Clip is a sub-resource under channel.
                Each clip represents a clipping
                operation that generates a VOD playlist
                from its channel given a set of
                timestamp ranges.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseGetClip._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_clip(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseGetClip._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseLivestreamServiceRestTransport._BaseGetClip._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = LivestreamServiceRestTransport._GetClip._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Clip()
            pb_resp = resources.Clip.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_clip(resp)
            return resp

    class _GetEvent(
        _BaseLivestreamServiceRestTransport._BaseGetEvent, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.GetEvent")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Event:
            r"""Call the get event method over HTTP.

            Args:
                request (~.service.GetEventRequest):
                    The request object. Request message for
                "LivestreamService.GetEvent".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Event:
                    Event is a sub-resource of a channel,
                which can be scheduled by the user to
                execute operations on a channel resource
                without having to stop the channel.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseGetEvent._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_event(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseGetEvent._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseGetEvent._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._GetEvent._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Event()
            pb_resp = resources.Event.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_event(resp)
            return resp

    class _GetInput(
        _BaseLivestreamServiceRestTransport._BaseGetInput, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.GetInput")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Input:
            r"""Call the get input method over HTTP.

            Args:
                request (~.service.GetInputRequest):
                    The request object. Request message for
                "LivestreamService.GetInput".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Input:
                    Input resource represents the
                endpoint from which the channel ingests
                the input stream.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseGetInput._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_input(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseGetInput._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseGetInput._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._GetInput._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Input()
            pb_resp = resources.Input.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_input(resp)
            return resp

    class _GetPool(
        _BaseLivestreamServiceRestTransport._BaseGetPool, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.GetPool")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetPoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resources.Pool:
            r"""Call the get pool method over HTTP.

            Args:
                request (~.service.GetPoolRequest):
                    The request object. Request message for
                "LivestreamService.GetPool".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resources.Pool:
                    Pool resource defines the
                configuration of Live Stream pools for a
                specific location. Currently we support
                only one pool resource per project per
                location. After the creation of the
                first input, a default pool is created
                automatically at
                "projects/{project}/locations/{location}/pools/default".

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseGetPool._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_pool(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseGetPool._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = (
                _BaseLivestreamServiceRestTransport._BaseGetPool._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = LivestreamServiceRestTransport._GetPool._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resources.Pool()
            pb_resp = resources.Pool.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_pool(resp)
            return resp

    class _ListAssets(
        _BaseLivestreamServiceRestTransport._BaseListAssets, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.ListAssets")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListAssetsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListAssetsResponse:
            r"""Call the list assets method over HTTP.

            Args:
                request (~.service.ListAssetsRequest):
                    The request object. Request message for
                "LivestreamService.ListAssets".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListAssetsResponse:
                    Response message for
                "LivestreamService.ListAssets".

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseListAssets._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_assets(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseListAssets._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseListAssets._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._ListAssets._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListAssetsResponse()
            pb_resp = service.ListAssetsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_assets(resp)
            return resp

    class _ListChannels(
        _BaseLivestreamServiceRestTransport._BaseListChannels, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.ListChannels")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListChannelsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListChannelsResponse:
            r"""Call the list channels method over HTTP.

            Args:
                request (~.service.ListChannelsRequest):
                    The request object. Request message for
                "LivestreamService.ListChannels".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListChannelsResponse:
                    Response message for
                "LivestreamService.ListChannels".

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseListChannels._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_channels(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseListChannels._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseListChannels._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._ListChannels._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListChannelsResponse()
            pb_resp = service.ListChannelsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_channels(resp)
            return resp

    class _ListClips(
        _BaseLivestreamServiceRestTransport._BaseListClips, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.ListClips")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListClipsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListClipsResponse:
            r"""Call the list clips method over HTTP.

            Args:
                request (~.service.ListClipsRequest):
                    The request object. Request message for
                "LivestreamService.ListClips".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListClipsResponse:
                    Response message for
                "LivestreamService.ListClips".

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseListClips._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_clips(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseListClips._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseListClips._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._ListClips._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListClipsResponse()
            pb_resp = service.ListClipsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_clips(resp)
            return resp

    class _ListEvents(
        _BaseLivestreamServiceRestTransport._BaseListEvents, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.ListEvents")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListEventsResponse:
            r"""Call the list events method over HTTP.

            Args:
                request (~.service.ListEventsRequest):
                    The request object. Request message for
                "LivestreamService.ListEvents".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListEventsResponse:
                    Response message for
                "LivestreamService.ListEvents".

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseListEvents._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_events(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseListEvents._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseListEvents._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._ListEvents._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListEventsResponse()
            pb_resp = service.ListEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_events(resp)
            return resp

    class _ListInputs(
        _BaseLivestreamServiceRestTransport._BaseListInputs, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.ListInputs")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListInputsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListInputsResponse:
            r"""Call the list inputs method over HTTP.

            Args:
                request (~.service.ListInputsRequest):
                    The request object. Request message for
                "LivestreamService.ListInputs".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListInputsResponse:
                    Response message for
                "LivestreamService.ListInputs".

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseListInputs._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_inputs(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseListInputs._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseListInputs._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._ListInputs._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListInputsResponse()
            pb_resp = service.ListInputsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_inputs(resp)
            return resp

    class _StartChannel(
        _BaseLivestreamServiceRestTransport._BaseStartChannel, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.StartChannel")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.StartChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the start channel method over HTTP.

            Args:
                request (~.service.StartChannelRequest):
                    The request object. Request message for
                "LivestreamService.StartChannel".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseStartChannel._get_http_options()
            )
            request, metadata = self._interceptor.pre_start_channel(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseStartChannel._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseStartChannel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseStartChannel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._StartChannel._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_start_channel(resp)
            return resp

    class _StopChannel(
        _BaseLivestreamServiceRestTransport._BaseStopChannel, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.StopChannel")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.StopChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the stop channel method over HTTP.

            Args:
                request (~.service.StopChannelRequest):
                    The request object. Request message for
                "LivestreamService.StopChannel".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseStopChannel._get_http_options()
            )
            request, metadata = self._interceptor.pre_stop_channel(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseStopChannel._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseStopChannel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseStopChannel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._StopChannel._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_stop_channel(resp)
            return resp

    class _UpdateChannel(
        _BaseLivestreamServiceRestTransport._BaseUpdateChannel,
        LivestreamServiceRestStub,
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.UpdateChannel")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.UpdateChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update channel method over HTTP.

            Args:
                request (~.service.UpdateChannelRequest):
                    The request object. Request message for
                "LivestreamService.UpdateChannel".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseUpdateChannel._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_channel(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseUpdateChannel._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseUpdateChannel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseUpdateChannel._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._UpdateChannel._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_channel(resp)
            return resp

    class _UpdateInput(
        _BaseLivestreamServiceRestTransport._BaseUpdateInput, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.UpdateInput")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.UpdateInputRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update input method over HTTP.

            Args:
                request (~.service.UpdateInputRequest):
                    The request object. Request message for
                "LivestreamService.UpdateInput".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseUpdateInput._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_input(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseUpdateInput._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseUpdateInput._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseUpdateInput._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._UpdateInput._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_input(resp)
            return resp

    class _UpdatePool(
        _BaseLivestreamServiceRestTransport._BaseUpdatePool, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.UpdatePool")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: service.UpdatePoolRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update pool method over HTTP.

            Args:
                request (~.service.UpdatePoolRequest):
                    The request object. Request message for
                "LivestreamService.UpdatePool".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseUpdatePool._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_pool(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseUpdatePool._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseUpdatePool._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseUpdatePool._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._UpdatePool._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_pool(resp)
            return resp

    @property
    def create_asset(
        self,
    ) -> Callable[[service.CreateAssetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_channel_(
        self,
    ) -> Callable[[service.CreateChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_clip(
        self,
    ) -> Callable[[service.CreateClipRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateClip(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_event(self) -> Callable[[service.CreateEventRequest], resources.Event]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_input(
        self,
    ) -> Callable[[service.CreateInputRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_asset(
        self,
    ) -> Callable[[service.DeleteAssetRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_channel(
        self,
    ) -> Callable[[service.DeleteChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_clip(
        self,
    ) -> Callable[[service.DeleteClipRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteClip(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_event(self) -> Callable[[service.DeleteEventRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_input(
        self,
    ) -> Callable[[service.DeleteInputRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_asset(self) -> Callable[[service.GetAssetRequest], resources.Asset]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetAsset(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_channel(self) -> Callable[[service.GetChannelRequest], resources.Channel]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_clip(self) -> Callable[[service.GetClipRequest], resources.Clip]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetClip(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_event(self) -> Callable[[service.GetEventRequest], resources.Event]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_input(self) -> Callable[[service.GetInputRequest], resources.Input]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_pool(self) -> Callable[[service.GetPoolRequest], resources.Pool]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetPool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_assets(
        self,
    ) -> Callable[[service.ListAssetsRequest], service.ListAssetsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAssets(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_channels(
        self,
    ) -> Callable[[service.ListChannelsRequest], service.ListChannelsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListChannels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_clips(
        self,
    ) -> Callable[[service.ListClipsRequest], service.ListClipsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListClips(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_events(
        self,
    ) -> Callable[[service.ListEventsRequest], service.ListEventsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_inputs(
        self,
    ) -> Callable[[service.ListInputsRequest], service.ListInputsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListInputs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def start_channel(
        self,
    ) -> Callable[[service.StartChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StartChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def stop_channel(
        self,
    ) -> Callable[[service.StopChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._StopChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_channel(
        self,
    ) -> Callable[[service.UpdateChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_input(
        self,
    ) -> Callable[[service.UpdateInputRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateInput(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_pool(
        self,
    ) -> Callable[[service.UpdatePoolRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdatePool(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(
        _BaseLivestreamServiceRestTransport._BaseGetLocation, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.GetLocation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.GetLocationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.Location:
            r"""Call the get location method over HTTP.

            Args:
                request (locations_pb2.GetLocationRequest):
                    The request object for GetLocation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.Location: Response from GetLocation method.
            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseGetLocation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseGetLocation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._GetLocation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.Location()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(
        _BaseLivestreamServiceRestTransport._BaseListLocations,
        LivestreamServiceRestStub,
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.ListLocations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: locations_pb2.ListLocationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> locations_pb2.ListLocationsResponse:
            r"""Call the list locations method over HTTP.

            Args:
                request (locations_pb2.ListLocationsRequest):
                    The request object for ListLocations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                locations_pb2.ListLocationsResponse: Response from ListLocations method.
            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseListLocations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseListLocations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._ListLocations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseLivestreamServiceRestTransport._BaseCancelOperation,
        LivestreamServiceRestStub,
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.CancelOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )
            return response

        def __call__(
            self,
            request: operations_pb2.CancelOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the cancel operation method over HTTP.

            Args:
                request (operations_pb2.CancelOperationRequest):
                    The request object for CancelOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseCancelOperation._get_transcoded_request(
                http_options, request
            )

            body = _BaseLivestreamServiceRestTransport._BaseCancelOperation._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseCancelOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._CancelOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
                body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(
        _BaseLivestreamServiceRestTransport._BaseDeleteOperation,
        LivestreamServiceRestStub,
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.DeleteOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.DeleteOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> None:
            r"""Call the delete operation method over HTTP.

            Args:
                request (operations_pb2.DeleteOperationRequest):
                    The request object for DeleteOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseDeleteOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseDeleteOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._DeleteOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(
        _BaseLivestreamServiceRestTransport._BaseGetOperation, LivestreamServiceRestStub
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.GetOperation")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.GetOperationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the get operation method over HTTP.

            Args:
                request (operations_pb2.GetOperationRequest):
                    The request object for GetOperation method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.Operation: Response from GetOperation method.
            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseGetOperation._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseGetOperation._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._GetOperation._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.Operation()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(
        _BaseLivestreamServiceRestTransport._BaseListOperations,
        LivestreamServiceRestStub,
    ):
        def __hash__(self):
            return hash("LivestreamServiceRestTransport.ListOperations")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: operations_pb2.ListOperationsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.ListOperationsResponse:
            r"""Call the list operations method over HTTP.

            Args:
                request (operations_pb2.ListOperationsRequest):
                    The request object for ListOperations method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                operations_pb2.ListOperationsResponse: Response from ListOperations method.
            """

            http_options = (
                _BaseLivestreamServiceRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = _BaseLivestreamServiceRestTransport._BaseListOperations._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseLivestreamServiceRestTransport._BaseListOperations._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = LivestreamServiceRestTransport._ListOperations._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            content = response.content.decode("utf-8")
            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("LivestreamServiceRestTransport",)
