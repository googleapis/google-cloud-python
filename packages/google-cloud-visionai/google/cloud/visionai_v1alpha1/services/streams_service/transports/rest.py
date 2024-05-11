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
import re
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import (
    gapic_v1,
    operations_v1,
    path_template,
    rest_helpers,
    rest_streaming,
)
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.longrunning import operations_pb2  # type: ignore

from google.cloud.visionai_v1alpha1.types import (
    common,
    streams_resources,
    streams_service,
)

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import StreamsServiceTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class StreamsServiceRestInterceptor:
    """Interceptor for StreamsService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the StreamsServiceRestTransport.

    .. code-block:: python
        class MyCustomStreamsServiceInterceptor(StreamsServiceRestInterceptor):
            def pre_create_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_series(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_series(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_stream(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_stream(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_series(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_series(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_stream(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_stream(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_generate_stream_hls_token(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_generate_stream_hls_token(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_series(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_series(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_stream(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_stream(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_clusters(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_clusters(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_events(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_events(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_series(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_series(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_streams(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_streams(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_materialize_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_materialize_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_cluster(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_cluster(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_event(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_event(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_series(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_series(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_stream(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_stream(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = StreamsServiceRestTransport(interceptor=MyCustomStreamsServiceInterceptor())
        client = StreamsServiceClient(transport=transport)


    """

    def pre_create_cluster(
        self,
        request: streams_service.CreateClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.CreateClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_create_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_cluster

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_create_event(
        self,
        request: streams_service.CreateEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.CreateEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_create_event(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_event

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_create_series(
        self,
        request: streams_service.CreateSeriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.CreateSeriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_series

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_create_series(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_series

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_create_stream(
        self,
        request: streams_service.CreateStreamRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.CreateStreamRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_stream

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_create_stream(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_stream

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_cluster(
        self,
        request: streams_service.DeleteClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.DeleteClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_delete_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_cluster

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_event(
        self,
        request: streams_service.DeleteEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.DeleteEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_delete_event(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_event

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_series(
        self,
        request: streams_service.DeleteSeriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.DeleteSeriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_series

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_delete_series(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_series

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_delete_stream(
        self,
        request: streams_service.DeleteStreamRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.DeleteStreamRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_stream

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_delete_stream(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_stream

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_generate_stream_hls_token(
        self,
        request: streams_service.GenerateStreamHlsTokenRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        streams_service.GenerateStreamHlsTokenRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for generate_stream_hls_token

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_generate_stream_hls_token(
        self, response: streams_service.GenerateStreamHlsTokenResponse
    ) -> streams_service.GenerateStreamHlsTokenResponse:
        """Post-rpc interceptor for generate_stream_hls_token

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_cluster(
        self,
        request: streams_service.GetClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.GetClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_get_cluster(self, response: common.Cluster) -> common.Cluster:
        """Post-rpc interceptor for get_cluster

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_event(
        self,
        request: streams_service.GetEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.GetEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_get_event(
        self, response: streams_resources.Event
    ) -> streams_resources.Event:
        """Post-rpc interceptor for get_event

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_series(
        self,
        request: streams_service.GetSeriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.GetSeriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_series

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_get_series(
        self, response: streams_resources.Series
    ) -> streams_resources.Series:
        """Post-rpc interceptor for get_series

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_stream(
        self,
        request: streams_service.GetStreamRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.GetStreamRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_stream

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_get_stream(
        self, response: streams_resources.Stream
    ) -> streams_resources.Stream:
        """Post-rpc interceptor for get_stream

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_clusters(
        self,
        request: streams_service.ListClustersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.ListClustersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_clusters

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_list_clusters(
        self, response: streams_service.ListClustersResponse
    ) -> streams_service.ListClustersResponse:
        """Post-rpc interceptor for list_clusters

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_events(
        self,
        request: streams_service.ListEventsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.ListEventsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_events

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_list_events(
        self, response: streams_service.ListEventsResponse
    ) -> streams_service.ListEventsResponse:
        """Post-rpc interceptor for list_events

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_series(
        self,
        request: streams_service.ListSeriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.ListSeriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_series

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_list_series(
        self, response: streams_service.ListSeriesResponse
    ) -> streams_service.ListSeriesResponse:
        """Post-rpc interceptor for list_series

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_streams(
        self,
        request: streams_service.ListStreamsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.ListStreamsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_streams

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_list_streams(
        self, response: streams_service.ListStreamsResponse
    ) -> streams_service.ListStreamsResponse:
        """Post-rpc interceptor for list_streams

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_materialize_channel(
        self,
        request: streams_service.MaterializeChannelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.MaterializeChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for materialize_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_materialize_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for materialize_channel

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_update_cluster(
        self,
        request: streams_service.UpdateClusterRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.UpdateClusterRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_cluster

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_update_cluster(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_cluster

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_update_event(
        self,
        request: streams_service.UpdateEventRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.UpdateEventRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_event

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_update_event(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_event

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_update_series(
        self,
        request: streams_service.UpdateSeriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.UpdateSeriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_series

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_update_series(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_series

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_update_stream(
        self,
        request: streams_service.UpdateStreamRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[streams_service.UpdateStreamRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_stream

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_update_stream(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_stream

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
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
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
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
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_iam_policy(
        self,
        request: iam_policy_pb2.GetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.GetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_set_iam_policy(
        self,
        request: iam_policy_pb2.SetIamPolicyRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.SetIamPolicyRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response

    def pre_test_iam_permissions(
        self,
        request: iam_policy_pb2.TestIamPermissionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[iam_policy_pb2.TestIamPermissionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
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
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
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
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
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
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
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
        before they are sent to the StreamsService server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the StreamsService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class StreamsServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: StreamsServiceRestInterceptor


class StreamsServiceRestTransport(StreamsServiceTransport):
    """REST backend transport for StreamsService.

    Service describing handlers for resources.
    Vision API and Vision AI API are two independent APIs developed
    by the same team. Vision API is for people to annotate their
    image while Vision AI is an e2e solution for customer to build
    their own computer vision application.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "visionai.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[StreamsServiceRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'visionai.googleapis.com').
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
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or StreamsServiceRestInterceptor()
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
                        "uri": "/v1alpha1/{name=projects/*/locations/*/operations/*}:cancel",
                        "body": "*",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v1alpha1/{name=projects/*/locations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v1alpha1/{name=projects/*/locations/*/operations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha1/{name=projects/*/locations/*/warehouseOperations/*}",
                    },
                    {
                        "method": "get",
                        "uri": "/v1alpha1/{name=projects/*/locations/*/corpora/*/assets/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v1alpha1/{name=projects/*/locations/*}/operations",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v1alpha1",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateCluster(StreamsServiceRestStub):
        def __hash__(self):
            return hash("CreateCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "clusterId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.CreateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create cluster method over HTTP.

            Args:
                request (~.streams_service.CreateClusterRequest):
                    The request object. Message for creating a Cluster.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha1/{parent=projects/*/locations/*}/clusters",
                    "body": "cluster",
                },
            ]
            request, metadata = self._interceptor.pre_create_cluster(request, metadata)
            pb_request = streams_service.CreateClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_cluster(resp)
            return resp

    class _CreateEvent(StreamsServiceRestStub):
        def __hash__(self):
            return hash("CreateEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "eventId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.CreateEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create event method over HTTP.

            Args:
                request (~.streams_service.CreateEventRequest):
                    The request object. Message for creating a Event.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha1/{parent=projects/*/locations/*/clusters/*}/events",
                    "body": "event",
                },
            ]
            request, metadata = self._interceptor.pre_create_event(request, metadata)
            pb_request = streams_service.CreateEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_event(resp)
            return resp

    class _CreateSeries(StreamsServiceRestStub):
        def __hash__(self):
            return hash("CreateSeries")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "seriesId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.CreateSeriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create series method over HTTP.

            Args:
                request (~.streams_service.CreateSeriesRequest):
                    The request object. Message for creating a Series.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha1/{parent=projects/*/locations/*/clusters/*}/series",
                    "body": "series",
                },
            ]
            request, metadata = self._interceptor.pre_create_series(request, metadata)
            pb_request = streams_service.CreateSeriesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_series(resp)
            return resp

    class _CreateStream(StreamsServiceRestStub):
        def __hash__(self):
            return hash("CreateStream")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "streamId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.CreateStreamRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create stream method over HTTP.

            Args:
                request (~.streams_service.CreateStreamRequest):
                    The request object. Message for creating a Stream.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha1/{parent=projects/*/locations/*/clusters/*}/streams",
                    "body": "stream",
                },
            ]
            request, metadata = self._interceptor.pre_create_stream(request, metadata)
            pb_request = streams_service.CreateStreamRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_stream(resp)
            return resp

    class _DeleteCluster(StreamsServiceRestStub):
        def __hash__(self):
            return hash("DeleteCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.DeleteClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete cluster method over HTTP.

            Args:
                request (~.streams_service.DeleteClusterRequest):
                    The request object. Message for deleting a Cluster.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/clusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_cluster(request, metadata)
            pb_request = streams_service.DeleteClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_cluster(resp)
            return resp

    class _DeleteEvent(StreamsServiceRestStub):
        def __hash__(self):
            return hash("DeleteEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.DeleteEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete event method over HTTP.

            Args:
                request (~.streams_service.DeleteEventRequest):
                    The request object. Message for deleting a Event.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/clusters/*/events/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_event(request, metadata)
            pb_request = streams_service.DeleteEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_event(resp)
            return resp

    class _DeleteSeries(StreamsServiceRestStub):
        def __hash__(self):
            return hash("DeleteSeries")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.DeleteSeriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete series method over HTTP.

            Args:
                request (~.streams_service.DeleteSeriesRequest):
                    The request object. Message for deleting a Series.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/clusters/*/series/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_series(request, metadata)
            pb_request = streams_service.DeleteSeriesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_series(resp)
            return resp

    class _DeleteStream(StreamsServiceRestStub):
        def __hash__(self):
            return hash("DeleteStream")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.DeleteStreamRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete stream method over HTTP.

            Args:
                request (~.streams_service.DeleteStreamRequest):
                    The request object. Message for deleting a Stream.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/clusters/*/streams/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_stream(request, metadata)
            pb_request = streams_service.DeleteStreamRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_stream(resp)
            return resp

    class _GenerateStreamHlsToken(StreamsServiceRestStub):
        def __hash__(self):
            return hash("GenerateStreamHlsToken")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.GenerateStreamHlsTokenRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> streams_service.GenerateStreamHlsTokenResponse:
            r"""Call the generate stream hls token method over HTTP.

            Args:
                request (~.streams_service.GenerateStreamHlsTokenRequest):
                    The request object. Request message for getting the auth
                token to access the stream HLS contents.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.streams_service.GenerateStreamHlsTokenResponse:
                    Response message for
                GenerateStreamHlsToken.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha1/{stream=projects/*/locations/*/clusters/*/streams/*}:generateStreamHlsToken",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_generate_stream_hls_token(
                request, metadata
            )
            pb_request = streams_service.GenerateStreamHlsTokenRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = streams_service.GenerateStreamHlsTokenResponse()
            pb_resp = streams_service.GenerateStreamHlsTokenResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_generate_stream_hls_token(resp)
            return resp

    class _GetCluster(StreamsServiceRestStub):
        def __hash__(self):
            return hash("GetCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.GetClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> common.Cluster:
            r"""Call the get cluster method over HTTP.

            Args:
                request (~.streams_service.GetClusterRequest):
                    The request object. Message for getting a Cluster.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.common.Cluster:
                    Message describing the Cluster
                object.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/clusters/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_cluster(request, metadata)
            pb_request = streams_service.GetClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = common.Cluster()
            pb_resp = common.Cluster.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_cluster(resp)
            return resp

    class _GetEvent(StreamsServiceRestStub):
        def __hash__(self):
            return hash("GetEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.GetEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> streams_resources.Event:
            r"""Call the get event method over HTTP.

            Args:
                request (~.streams_service.GetEventRequest):
                    The request object. Message for getting a Event.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.streams_resources.Event:
                    Message describing the Event object.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/clusters/*/events/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_event(request, metadata)
            pb_request = streams_service.GetEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = streams_resources.Event()
            pb_resp = streams_resources.Event.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_event(resp)
            return resp

    class _GetSeries(StreamsServiceRestStub):
        def __hash__(self):
            return hash("GetSeries")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.GetSeriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> streams_resources.Series:
            r"""Call the get series method over HTTP.

            Args:
                request (~.streams_service.GetSeriesRequest):
                    The request object. Message for getting a Series.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.streams_resources.Series:
                    Message describing the Series object.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/clusters/*/series/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_series(request, metadata)
            pb_request = streams_service.GetSeriesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = streams_resources.Series()
            pb_resp = streams_resources.Series.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_series(resp)
            return resp

    class _GetStream(StreamsServiceRestStub):
        def __hash__(self):
            return hash("GetStream")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.GetStreamRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> streams_resources.Stream:
            r"""Call the get stream method over HTTP.

            Args:
                request (~.streams_service.GetStreamRequest):
                    The request object. Message for getting a Stream.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.streams_resources.Stream:
                    Message describing the Stream object.
                The Stream and the Event resources are
                many to many; i.e., each Stream resource
                can associate to many Event resources
                and each Event resource can associate to
                many Stream resources.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/clusters/*/streams/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_stream(request, metadata)
            pb_request = streams_service.GetStreamRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = streams_resources.Stream()
            pb_resp = streams_resources.Stream.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_stream(resp)
            return resp

    class _ListClusters(StreamsServiceRestStub):
        def __hash__(self):
            return hash("ListClusters")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.ListClustersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> streams_service.ListClustersResponse:
            r"""Call the list clusters method over HTTP.

            Args:
                request (~.streams_service.ListClustersRequest):
                    The request object. Message for requesting list of
                Clusters.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.streams_service.ListClustersResponse:
                    Message for response to listing
                Clusters.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{parent=projects/*/locations/*}/clusters",
                },
            ]
            request, metadata = self._interceptor.pre_list_clusters(request, metadata)
            pb_request = streams_service.ListClustersRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = streams_service.ListClustersResponse()
            pb_resp = streams_service.ListClustersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_clusters(resp)
            return resp

    class _ListEvents(StreamsServiceRestStub):
        def __hash__(self):
            return hash("ListEvents")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.ListEventsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> streams_service.ListEventsResponse:
            r"""Call the list events method over HTTP.

            Args:
                request (~.streams_service.ListEventsRequest):
                    The request object. Message for requesting list of
                Events.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.streams_service.ListEventsResponse:
                    Message for response to listing
                Events.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{parent=projects/*/locations/*/clusters/*}/events",
                },
            ]
            request, metadata = self._interceptor.pre_list_events(request, metadata)
            pb_request = streams_service.ListEventsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = streams_service.ListEventsResponse()
            pb_resp = streams_service.ListEventsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_events(resp)
            return resp

    class _ListSeries(StreamsServiceRestStub):
        def __hash__(self):
            return hash("ListSeries")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.ListSeriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> streams_service.ListSeriesResponse:
            r"""Call the list series method over HTTP.

            Args:
                request (~.streams_service.ListSeriesRequest):
                    The request object. Message for requesting list of
                Series.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.streams_service.ListSeriesResponse:
                    Message for response to listing
                Series.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{parent=projects/*/locations/*/clusters/*}/series",
                },
            ]
            request, metadata = self._interceptor.pre_list_series(request, metadata)
            pb_request = streams_service.ListSeriesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = streams_service.ListSeriesResponse()
            pb_resp = streams_service.ListSeriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_series(resp)
            return resp

    class _ListStreams(StreamsServiceRestStub):
        def __hash__(self):
            return hash("ListStreams")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.ListStreamsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> streams_service.ListStreamsResponse:
            r"""Call the list streams method over HTTP.

            Args:
                request (~.streams_service.ListStreamsRequest):
                    The request object. Message for requesting list of
                Streams.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.streams_service.ListStreamsResponse:
                    Message for response to listing
                Streams.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{parent=projects/*/locations/*/clusters/*}/streams",
                },
            ]
            request, metadata = self._interceptor.pre_list_streams(request, metadata)
            pb_request = streams_service.ListStreamsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = streams_service.ListStreamsResponse()
            pb_resp = streams_service.ListStreamsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_streams(resp)
            return resp

    class _MaterializeChannel(StreamsServiceRestStub):
        def __hash__(self):
            return hash("MaterializeChannel")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "channelId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.MaterializeChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the materialize channel method over HTTP.

            Args:
                request (~.streams_service.MaterializeChannelRequest):
                    The request object. Message for materializing a channel.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha1/{parent=projects/*/locations/*/clusters/*}/channels",
                    "body": "channel",
                },
            ]
            request, metadata = self._interceptor.pre_materialize_channel(
                request, metadata
            )
            pb_request = streams_service.MaterializeChannelRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_materialize_channel(resp)
            return resp

    class _UpdateCluster(StreamsServiceRestStub):
        def __hash__(self):
            return hash("UpdateCluster")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.UpdateClusterRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update cluster method over HTTP.

            Args:
                request (~.streams_service.UpdateClusterRequest):
                    The request object. Message for updating a Cluster.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha1/{cluster.name=projects/*/locations/*/clusters/*}",
                    "body": "cluster",
                },
            ]
            request, metadata = self._interceptor.pre_update_cluster(request, metadata)
            pb_request = streams_service.UpdateClusterRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_cluster(resp)
            return resp

    class _UpdateEvent(StreamsServiceRestStub):
        def __hash__(self):
            return hash("UpdateEvent")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.UpdateEventRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update event method over HTTP.

            Args:
                request (~.streams_service.UpdateEventRequest):
                    The request object. Message for updating a Event.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha1/{event.name=projects/*/locations/*/clusters/*/events/*}",
                    "body": "event",
                },
            ]
            request, metadata = self._interceptor.pre_update_event(request, metadata)
            pb_request = streams_service.UpdateEventRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_event(resp)
            return resp

    class _UpdateSeries(StreamsServiceRestStub):
        def __hash__(self):
            return hash("UpdateSeries")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.UpdateSeriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update series method over HTTP.

            Args:
                request (~.streams_service.UpdateSeriesRequest):
                    The request object. Message for updating a Series.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha1/{series.name=projects/*/locations/*/clusters/*/series/*}",
                    "body": "series",
                },
            ]
            request, metadata = self._interceptor.pre_update_series(request, metadata)
            pb_request = streams_service.UpdateSeriesRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_series(resp)
            return resp

    class _UpdateStream(StreamsServiceRestStub):
        def __hash__(self):
            return hash("UpdateStream")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "updateMask": {},
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: streams_service.UpdateStreamRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update stream method over HTTP.

            Args:
                request (~.streams_service.UpdateStreamRequest):
                    The request object. Message for updating a Stream.
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1alpha1/{stream.name=projects/*/locations/*/clusters/*/streams/*}",
                    "body": "stream",
                },
            ]
            request, metadata = self._interceptor.pre_update_stream(request, metadata)
            pb_request = streams_service.UpdateStreamRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"], use_integers_for_enums=True
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    use_integers_for_enums=True,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            query_params["$alt"] = "json;enum-encoding=int"

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_stream(resp)
            return resp

    @property
    def create_cluster(
        self,
    ) -> Callable[[streams_service.CreateClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_event(
        self,
    ) -> Callable[[streams_service.CreateEventRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_series(
        self,
    ) -> Callable[[streams_service.CreateSeriesRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSeries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_stream(
        self,
    ) -> Callable[[streams_service.CreateStreamRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateStream(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_cluster(
        self,
    ) -> Callable[[streams_service.DeleteClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_event(
        self,
    ) -> Callable[[streams_service.DeleteEventRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_series(
        self,
    ) -> Callable[[streams_service.DeleteSeriesRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteSeries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_stream(
        self,
    ) -> Callable[[streams_service.DeleteStreamRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteStream(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def generate_stream_hls_token(
        self,
    ) -> Callable[
        [streams_service.GenerateStreamHlsTokenRequest],
        streams_service.GenerateStreamHlsTokenResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GenerateStreamHlsToken(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_cluster(
        self,
    ) -> Callable[[streams_service.GetClusterRequest], common.Cluster]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_event(
        self,
    ) -> Callable[[streams_service.GetEventRequest], streams_resources.Event]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_series(
        self,
    ) -> Callable[[streams_service.GetSeriesRequest], streams_resources.Series]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSeries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_stream(
        self,
    ) -> Callable[[streams_service.GetStreamRequest], streams_resources.Stream]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetStream(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_clusters(
        self,
    ) -> Callable[
        [streams_service.ListClustersRequest], streams_service.ListClustersResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListClusters(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_events(
        self,
    ) -> Callable[
        [streams_service.ListEventsRequest], streams_service.ListEventsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListEvents(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_series(
        self,
    ) -> Callable[
        [streams_service.ListSeriesRequest], streams_service.ListSeriesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSeries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_streams(
        self,
    ) -> Callable[
        [streams_service.ListStreamsRequest], streams_service.ListStreamsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListStreams(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def materialize_channel(
        self,
    ) -> Callable[
        [streams_service.MaterializeChannelRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._MaterializeChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_cluster(
        self,
    ) -> Callable[[streams_service.UpdateClusterRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateCluster(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_event(
        self,
    ) -> Callable[[streams_service.UpdateEventRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateEvent(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_series(
        self,
    ) -> Callable[[streams_service.UpdateSeriesRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSeries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_stream(
        self,
    ) -> Callable[[streams_service.UpdateStreamRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateStream(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(StreamsServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{name=projects/*/locations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_location(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.Location()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_location(resp)
            return resp

    @property
    def list_locations(self):
        return self._ListLocations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListLocations(StreamsServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{name=projects/*}/locations",
                },
            ]

            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = locations_pb2.ListLocationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_locations(resp)
            return resp

    @property
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(StreamsServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.GetIamPolicyRequest):
                    The request object for GetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from GetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/streams/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/events/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/series/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/operators/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/operators/*/versions/*}:getIamPolicy",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/analyses/*}:getIamPolicy",
                },
            ]

            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(StreamsServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (iam_policy_pb2.SetIamPolicyRequest):
                    The request object for SetIamPolicy method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                policy_pb2.Policy: Response from SetIamPolicy method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/streams/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/events/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/series/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/operators/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/operators/*/versions/*}:setIamPolicy",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/analyses/*}:setIamPolicy",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = policy_pb2.Policy()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(StreamsServiceRestStub):
        def __call__(
            self,
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (iam_policy_pb2.TestIamPermissionsRequest):
                    The request object for TestIamPermissions method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                iam_policy_pb2.TestIamPermissionsResponse: Response from TestIamPermissions method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/streams/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/events/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/series/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/operators/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/operators/*/versions/*}:testIamPermissions",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v1alpha1/{resource=projects/*/locations/*/clusters/*/analyses/*}:testIamPermissions",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(StreamsServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/operations/*}:cancel",
                    "body": "*",
                },
            ]

            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            body = json.dumps(transcoded_request["body"])
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_cancel_operation(None)

    @property
    def delete_operation(self):
        return self._DeleteOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _DeleteOperation(StreamsServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            return self._interceptor.post_delete_operation(None)

    @property
    def get_operation(self):
        return self._GetOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetOperation(StreamsServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/operations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/warehouseOperations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v1alpha1/{name=projects/*/locations/*/corpora/*/assets/*/operations/*}",
                },
            ]

            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.Operation()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_get_operation(resp)
            return resp

    @property
    def list_operations(self):
        return self._ListOperations(self._session, self._host, self._interceptor)  # type: ignore

    class _ListOperations(StreamsServiceRestStub):
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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1alpha1/{name=projects/*/locations/*}/operations",
                },
            ]

            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            request_kwargs = json_format.MessageToDict(request)
            transcoded_request = path_template.transcode(http_options, **request_kwargs)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(json.dumps(transcoded_request["query_params"]))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"

            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            resp = operations_pb2.ListOperationsResponse()
            resp = json_format.Parse(response.content.decode("utf-8"), resp)
            resp = self._interceptor.post_list_operations(resp)
            return resp

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("StreamsServiceRestTransport",)
