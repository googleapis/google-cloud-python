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
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.cloud.eventarc_v1.types import (
    channel,
    channel_connection,
    discovery,
    eventarc,
)
from google.cloud.eventarc_v1.types import (
    google_channel_config as gce_google_channel_config,
)
from google.cloud.eventarc_v1.types import google_channel_config
from google.cloud.eventarc_v1.types import trigger

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseEventarcRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class EventarcRestInterceptor:
    """Interceptor for Eventarc.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the EventarcRestTransport.

    .. code-block:: python
        class MyCustomEventarcInterceptor(EventarcRestInterceptor):
            def pre_create_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_channel_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_channel_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_channel_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_channel_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_channel_connection(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_channel_connection(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_google_channel_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_google_channel_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_provider(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_provider(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_channel_connections(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_channel_connections(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_channels(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_channels(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_providers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_providers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_triggers(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_triggers(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_channel(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_channel(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_google_channel_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_google_channel_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_trigger(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_trigger(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = EventarcRestTransport(interceptor=MyCustomEventarcInterceptor())
        client = EventarcClient(transport=transport)


    """

    def pre_create_channel(
        self,
        request: eventarc.CreateChannelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.CreateChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_create_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_channel

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_create_channel_connection(
        self,
        request: eventarc.CreateChannelConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.CreateChannelConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_channel_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_create_channel_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_channel_connection

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_create_trigger(
        self,
        request: eventarc.CreateTriggerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.CreateTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_create_trigger(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_trigger

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_delete_channel(
        self,
        request: eventarc.DeleteChannelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.DeleteChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_delete_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_channel

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_delete_channel_connection(
        self,
        request: eventarc.DeleteChannelConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.DeleteChannelConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_channel_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_delete_channel_connection(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_channel_connection

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_delete_trigger(
        self,
        request: eventarc.DeleteTriggerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.DeleteTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_delete_trigger(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_trigger

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_get_channel(
        self, request: eventarc.GetChannelRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[eventarc.GetChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_get_channel(self, response: channel.Channel) -> channel.Channel:
        """Post-rpc interceptor for get_channel

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_get_channel_connection(
        self,
        request: eventarc.GetChannelConnectionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.GetChannelConnectionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_channel_connection

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_get_channel_connection(
        self, response: channel_connection.ChannelConnection
    ) -> channel_connection.ChannelConnection:
        """Post-rpc interceptor for get_channel_connection

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_get_google_channel_config(
        self,
        request: eventarc.GetGoogleChannelConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.GetGoogleChannelConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_google_channel_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_get_google_channel_config(
        self, response: google_channel_config.GoogleChannelConfig
    ) -> google_channel_config.GoogleChannelConfig:
        """Post-rpc interceptor for get_google_channel_config

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_get_provider(
        self, request: eventarc.GetProviderRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[eventarc.GetProviderRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_provider

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_get_provider(self, response: discovery.Provider) -> discovery.Provider:
        """Post-rpc interceptor for get_provider

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_get_trigger(
        self, request: eventarc.GetTriggerRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[eventarc.GetTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_get_trigger(self, response: trigger.Trigger) -> trigger.Trigger:
        """Post-rpc interceptor for get_trigger

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_list_channel_connections(
        self,
        request: eventarc.ListChannelConnectionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.ListChannelConnectionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_channel_connections

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_list_channel_connections(
        self, response: eventarc.ListChannelConnectionsResponse
    ) -> eventarc.ListChannelConnectionsResponse:
        """Post-rpc interceptor for list_channel_connections

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_list_channels(
        self, request: eventarc.ListChannelsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[eventarc.ListChannelsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_channels

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_list_channels(
        self, response: eventarc.ListChannelsResponse
    ) -> eventarc.ListChannelsResponse:
        """Post-rpc interceptor for list_channels

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_list_providers(
        self,
        request: eventarc.ListProvidersRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.ListProvidersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_providers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_list_providers(
        self, response: eventarc.ListProvidersResponse
    ) -> eventarc.ListProvidersResponse:
        """Post-rpc interceptor for list_providers

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_list_triggers(
        self, request: eventarc.ListTriggersRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[eventarc.ListTriggersRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_triggers

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_list_triggers(
        self, response: eventarc.ListTriggersResponse
    ) -> eventarc.ListTriggersResponse:
        """Post-rpc interceptor for list_triggers

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_update_channel(
        self,
        request: eventarc.UpdateChannelRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.UpdateChannelRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_channel

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_update_channel(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_channel

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_update_google_channel_config(
        self,
        request: eventarc.UpdateGoogleChannelConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.UpdateGoogleChannelConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_google_channel_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_update_google_channel_config(
        self, response: gce_google_channel_config.GoogleChannelConfig
    ) -> gce_google_channel_config.GoogleChannelConfig:
        """Post-rpc interceptor for update_google_channel_config

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response

    def pre_update_trigger(
        self,
        request: eventarc.UpdateTriggerRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[eventarc.UpdateTriggerRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_trigger

        Override in a subclass to manipulate the request or metadata
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_update_trigger(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_trigger

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
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
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_get_location(
        self, response: locations_pb2.Location
    ) -> locations_pb2.Location:
        """Post-rpc interceptor for get_location

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
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
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_list_locations(
        self, response: locations_pb2.ListLocationsResponse
    ) -> locations_pb2.ListLocationsResponse:
        """Post-rpc interceptor for list_locations

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
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
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
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
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
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
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
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
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
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
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
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
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
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
        before they are sent to the Eventarc server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the Eventarc server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class EventarcRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: EventarcRestInterceptor


class EventarcRestTransport(_BaseEventarcRestTransport):
    """REST backend synchronous transport for Eventarc.

    Eventarc allows users to subscribe to various events that are
    provided by Google Cloud services and forward them to supported
    destinations.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "eventarc.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[EventarcRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'eventarc.googleapis.com').
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
        self._interceptor = interceptor or EventarcRestInterceptor()
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

    class _CreateChannel(
        _BaseEventarcRestTransport._BaseCreateChannel, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.CreateChannel")

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
            request: eventarc.CreateChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create channel method over HTTP.

            Args:
                request (~.eventarc.CreateChannelRequest):
                    The request object. The request message for the
                CreateChannel method.
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
                _BaseEventarcRestTransport._BaseCreateChannel._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_channel(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseCreateChannel._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseEventarcRestTransport._BaseCreateChannel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseCreateChannel._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._CreateChannel._get_response(
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

    class _CreateChannelConnection(
        _BaseEventarcRestTransport._BaseCreateChannelConnection, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.CreateChannelConnection")

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
            request: eventarc.CreateChannelConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create channel connection method over HTTP.

            Args:
                request (~.eventarc.CreateChannelConnectionRequest):
                    The request object. The request message for the
                CreateChannelConnection method.
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
                _BaseEventarcRestTransport._BaseCreateChannelConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_channel_connection(
                request, metadata
            )
            transcoded_request = _BaseEventarcRestTransport._BaseCreateChannelConnection._get_transcoded_request(
                http_options, request
            )

            body = _BaseEventarcRestTransport._BaseCreateChannelConnection._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEventarcRestTransport._BaseCreateChannelConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EventarcRestTransport._CreateChannelConnection._get_response(
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
            resp = self._interceptor.post_create_channel_connection(resp)
            return resp

    class _CreateTrigger(
        _BaseEventarcRestTransport._BaseCreateTrigger, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.CreateTrigger")

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
            request: eventarc.CreateTriggerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create trigger method over HTTP.

            Args:
                request (~.eventarc.CreateTriggerRequest):
                    The request object. The request message for the
                CreateTrigger method.
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
                _BaseEventarcRestTransport._BaseCreateTrigger._get_http_options()
            )
            request, metadata = self._interceptor.pre_create_trigger(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseCreateTrigger._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseEventarcRestTransport._BaseCreateTrigger._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseCreateTrigger._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._CreateTrigger._get_response(
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
            resp = self._interceptor.post_create_trigger(resp)
            return resp

    class _DeleteChannel(
        _BaseEventarcRestTransport._BaseDeleteChannel, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.DeleteChannel")

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
            request: eventarc.DeleteChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete channel method over HTTP.

            Args:
                request (~.eventarc.DeleteChannelRequest):
                    The request object. The request message for the
                DeleteChannel method.
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
                _BaseEventarcRestTransport._BaseDeleteChannel._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_channel(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseDeleteChannel._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseDeleteChannel._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._DeleteChannel._get_response(
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

    class _DeleteChannelConnection(
        _BaseEventarcRestTransport._BaseDeleteChannelConnection, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.DeleteChannelConnection")

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
            request: eventarc.DeleteChannelConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete channel connection method over HTTP.

            Args:
                request (~.eventarc.DeleteChannelConnectionRequest):
                    The request object. The request message for the
                DeleteChannelConnection method.
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
                _BaseEventarcRestTransport._BaseDeleteChannelConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_channel_connection(
                request, metadata
            )
            transcoded_request = _BaseEventarcRestTransport._BaseDeleteChannelConnection._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEventarcRestTransport._BaseDeleteChannelConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EventarcRestTransport._DeleteChannelConnection._get_response(
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
            resp = self._interceptor.post_delete_channel_connection(resp)
            return resp

    class _DeleteTrigger(
        _BaseEventarcRestTransport._BaseDeleteTrigger, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.DeleteTrigger")

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
            request: eventarc.DeleteTriggerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete trigger method over HTTP.

            Args:
                request (~.eventarc.DeleteTriggerRequest):
                    The request object. The request message for the
                DeleteTrigger method.
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
                _BaseEventarcRestTransport._BaseDeleteTrigger._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_trigger(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseDeleteTrigger._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseDeleteTrigger._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._DeleteTrigger._get_response(
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
            resp = self._interceptor.post_delete_trigger(resp)
            return resp

    class _GetChannel(_BaseEventarcRestTransport._BaseGetChannel, EventarcRestStub):
        def __hash__(self):
            return hash("EventarcRestTransport.GetChannel")

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
            request: eventarc.GetChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> channel.Channel:
            r"""Call the get channel method over HTTP.

            Args:
                request (~.eventarc.GetChannelRequest):
                    The request object. The request message for the
                GetChannel method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.channel.Channel:
                    A representation of the Channel
                resource. A Channel is a resource on
                which event providers publish their
                events. The published events are
                delivered through the transport
                associated with the channel. Note that a
                channel is associated with exactly one
                event provider.

            """

            http_options = (
                _BaseEventarcRestTransport._BaseGetChannel._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_channel(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseGetChannel._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseGetChannel._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._GetChannel._get_response(
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
            resp = channel.Channel()
            pb_resp = channel.Channel.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_channel(resp)
            return resp

    class _GetChannelConnection(
        _BaseEventarcRestTransport._BaseGetChannelConnection, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.GetChannelConnection")

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
            request: eventarc.GetChannelConnectionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> channel_connection.ChannelConnection:
            r"""Call the get channel connection method over HTTP.

            Args:
                request (~.eventarc.GetChannelConnectionRequest):
                    The request object. The request message for the
                GetChannelConnection method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.channel_connection.ChannelConnection:
                    A representation of the
                ChannelConnection resource. A
                ChannelConnection is a resource which
                event providers create during the
                activation process to establish a
                connection between the provider and the
                subscriber channel.

            """

            http_options = (
                _BaseEventarcRestTransport._BaseGetChannelConnection._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_channel_connection(
                request, metadata
            )
            transcoded_request = _BaseEventarcRestTransport._BaseGetChannelConnection._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEventarcRestTransport._BaseGetChannelConnection._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EventarcRestTransport._GetChannelConnection._get_response(
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
            resp = channel_connection.ChannelConnection()
            pb_resp = channel_connection.ChannelConnection.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_channel_connection(resp)
            return resp

    class _GetGoogleChannelConfig(
        _BaseEventarcRestTransport._BaseGetGoogleChannelConfig, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.GetGoogleChannelConfig")

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
            request: eventarc.GetGoogleChannelConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> google_channel_config.GoogleChannelConfig:
            r"""Call the get google channel config method over HTTP.

            Args:
                request (~.eventarc.GetGoogleChannelConfigRequest):
                    The request object. The request message for the
                GetGoogleChannelConfig method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.google_channel_config.GoogleChannelConfig:
                    A GoogleChannelConfig is a resource
                that stores the custom settings
                respected by Eventarc first-party
                triggers in the matching region. Once
                configured, first-party event data will
                be protected using the specified custom
                managed encryption key instead of
                Google-managed encryption keys.

            """

            http_options = (
                _BaseEventarcRestTransport._BaseGetGoogleChannelConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_google_channel_config(
                request, metadata
            )
            transcoded_request = _BaseEventarcRestTransport._BaseGetGoogleChannelConfig._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEventarcRestTransport._BaseGetGoogleChannelConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EventarcRestTransport._GetGoogleChannelConfig._get_response(
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
            resp = google_channel_config.GoogleChannelConfig()
            pb_resp = google_channel_config.GoogleChannelConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_google_channel_config(resp)
            return resp

    class _GetProvider(_BaseEventarcRestTransport._BaseGetProvider, EventarcRestStub):
        def __hash__(self):
            return hash("EventarcRestTransport.GetProvider")

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
            request: eventarc.GetProviderRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> discovery.Provider:
            r"""Call the get provider method over HTTP.

            Args:
                request (~.eventarc.GetProviderRequest):
                    The request object. The request message for the
                GetProvider method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.discovery.Provider:
                    A representation of the Provider
                resource.

            """

            http_options = (
                _BaseEventarcRestTransport._BaseGetProvider._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_provider(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseGetProvider._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseGetProvider._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._GetProvider._get_response(
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
            resp = discovery.Provider()
            pb_resp = discovery.Provider.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_provider(resp)
            return resp

    class _GetTrigger(_BaseEventarcRestTransport._BaseGetTrigger, EventarcRestStub):
        def __hash__(self):
            return hash("EventarcRestTransport.GetTrigger")

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
            request: eventarc.GetTriggerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> trigger.Trigger:
            r"""Call the get trigger method over HTTP.

            Args:
                request (~.eventarc.GetTriggerRequest):
                    The request object. The request message for the
                GetTrigger method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.trigger.Trigger:
                    A representation of the trigger
                resource.

            """

            http_options = (
                _BaseEventarcRestTransport._BaseGetTrigger._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_trigger(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseGetTrigger._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseGetTrigger._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._GetTrigger._get_response(
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
            resp = trigger.Trigger()
            pb_resp = trigger.Trigger.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_trigger(resp)
            return resp

    class _ListChannelConnections(
        _BaseEventarcRestTransport._BaseListChannelConnections, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.ListChannelConnections")

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
            request: eventarc.ListChannelConnectionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> eventarc.ListChannelConnectionsResponse:
            r"""Call the list channel connections method over HTTP.

            Args:
                request (~.eventarc.ListChannelConnectionsRequest):
                    The request object. The request message for the
                ListChannelConnections method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.eventarc.ListChannelConnectionsResponse:
                    The response message for the ``ListChannelConnections``
                method.

            """

            http_options = (
                _BaseEventarcRestTransport._BaseListChannelConnections._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_channel_connections(
                request, metadata
            )
            transcoded_request = _BaseEventarcRestTransport._BaseListChannelConnections._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseEventarcRestTransport._BaseListChannelConnections._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EventarcRestTransport._ListChannelConnections._get_response(
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
            resp = eventarc.ListChannelConnectionsResponse()
            pb_resp = eventarc.ListChannelConnectionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_channel_connections(resp)
            return resp

    class _ListChannels(_BaseEventarcRestTransport._BaseListChannels, EventarcRestStub):
        def __hash__(self):
            return hash("EventarcRestTransport.ListChannels")

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
            request: eventarc.ListChannelsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> eventarc.ListChannelsResponse:
            r"""Call the list channels method over HTTP.

            Args:
                request (~.eventarc.ListChannelsRequest):
                    The request object. The request message for the
                ListChannels method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.eventarc.ListChannelsResponse:
                    The response message for the ``ListChannels`` method.
            """

            http_options = (
                _BaseEventarcRestTransport._BaseListChannels._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_channels(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseListChannels._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseListChannels._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._ListChannels._get_response(
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
            resp = eventarc.ListChannelsResponse()
            pb_resp = eventarc.ListChannelsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_channels(resp)
            return resp

    class _ListProviders(
        _BaseEventarcRestTransport._BaseListProviders, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.ListProviders")

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
            request: eventarc.ListProvidersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> eventarc.ListProvidersResponse:
            r"""Call the list providers method over HTTP.

            Args:
                request (~.eventarc.ListProvidersRequest):
                    The request object. The request message for the
                ListProviders method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.eventarc.ListProvidersResponse:
                    The response message for the ``ListProviders`` method.
            """

            http_options = (
                _BaseEventarcRestTransport._BaseListProviders._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_providers(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseListProviders._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseListProviders._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._ListProviders._get_response(
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
            resp = eventarc.ListProvidersResponse()
            pb_resp = eventarc.ListProvidersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_providers(resp)
            return resp

    class _ListTriggers(_BaseEventarcRestTransport._BaseListTriggers, EventarcRestStub):
        def __hash__(self):
            return hash("EventarcRestTransport.ListTriggers")

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
            request: eventarc.ListTriggersRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> eventarc.ListTriggersResponse:
            r"""Call the list triggers method over HTTP.

            Args:
                request (~.eventarc.ListTriggersRequest):
                    The request object. The request message for the
                ListTriggers method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.eventarc.ListTriggersResponse:
                    The response message for the ``ListTriggers`` method.
            """

            http_options = (
                _BaseEventarcRestTransport._BaseListTriggers._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_triggers(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseListTriggers._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseListTriggers._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._ListTriggers._get_response(
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
            resp = eventarc.ListTriggersResponse()
            pb_resp = eventarc.ListTriggersResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_triggers(resp)
            return resp

    class _UpdateChannel(
        _BaseEventarcRestTransport._BaseUpdateChannel, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.UpdateChannel")

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
            request: eventarc.UpdateChannelRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update channel method over HTTP.

            Args:
                request (~.eventarc.UpdateChannelRequest):
                    The request object. The request message for the
                UpdateChannel method.
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
                _BaseEventarcRestTransport._BaseUpdateChannel._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_channel(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseUpdateChannel._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseEventarcRestTransport._BaseUpdateChannel._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseUpdateChannel._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._UpdateChannel._get_response(
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

    class _UpdateGoogleChannelConfig(
        _BaseEventarcRestTransport._BaseUpdateGoogleChannelConfig, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.UpdateGoogleChannelConfig")

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
            request: eventarc.UpdateGoogleChannelConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gce_google_channel_config.GoogleChannelConfig:
            r"""Call the update google channel
            config method over HTTP.

                Args:
                    request (~.eventarc.UpdateGoogleChannelConfigRequest):
                        The request object. The request message for the
                    UpdateGoogleChannelConfig method.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gce_google_channel_config.GoogleChannelConfig:
                        A GoogleChannelConfig is a resource
                    that stores the custom settings
                    respected by Eventarc first-party
                    triggers in the matching region. Once
                    configured, first-party event data will
                    be protected using the specified custom
                    managed encryption key instead of
                    Google-managed encryption keys.

            """

            http_options = (
                _BaseEventarcRestTransport._BaseUpdateGoogleChannelConfig._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_google_channel_config(
                request, metadata
            )
            transcoded_request = _BaseEventarcRestTransport._BaseUpdateGoogleChannelConfig._get_transcoded_request(
                http_options, request
            )

            body = _BaseEventarcRestTransport._BaseUpdateGoogleChannelConfig._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEventarcRestTransport._BaseUpdateGoogleChannelConfig._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EventarcRestTransport._UpdateGoogleChannelConfig._get_response(
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
            resp = gce_google_channel_config.GoogleChannelConfig()
            pb_resp = gce_google_channel_config.GoogleChannelConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_google_channel_config(resp)
            return resp

    class _UpdateTrigger(
        _BaseEventarcRestTransport._BaseUpdateTrigger, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.UpdateTrigger")

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
            request: eventarc.UpdateTriggerRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update trigger method over HTTP.

            Args:
                request (~.eventarc.UpdateTriggerRequest):
                    The request object. The request message for the
                UpdateTrigger method.
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
                _BaseEventarcRestTransport._BaseUpdateTrigger._get_http_options()
            )
            request, metadata = self._interceptor.pre_update_trigger(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseUpdateTrigger._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseEventarcRestTransport._BaseUpdateTrigger._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseUpdateTrigger._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._UpdateTrigger._get_response(
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
            resp = self._interceptor.post_update_trigger(resp)
            return resp

    @property
    def create_channel_(
        self,
    ) -> Callable[[eventarc.CreateChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_channel_connection(
        self,
    ) -> Callable[[eventarc.CreateChannelConnectionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateChannelConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_trigger(
        self,
    ) -> Callable[[eventarc.CreateTriggerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateTrigger(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_channel(
        self,
    ) -> Callable[[eventarc.DeleteChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_channel_connection(
        self,
    ) -> Callable[[eventarc.DeleteChannelConnectionRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteChannelConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_trigger(
        self,
    ) -> Callable[[eventarc.DeleteTriggerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteTrigger(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_channel(self) -> Callable[[eventarc.GetChannelRequest], channel.Channel]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_channel_connection(
        self,
    ) -> Callable[
        [eventarc.GetChannelConnectionRequest], channel_connection.ChannelConnection
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetChannelConnection(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_google_channel_config(
        self,
    ) -> Callable[
        [eventarc.GetGoogleChannelConfigRequest],
        google_channel_config.GoogleChannelConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetGoogleChannelConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_provider(
        self,
    ) -> Callable[[eventarc.GetProviderRequest], discovery.Provider]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetProvider(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_trigger(self) -> Callable[[eventarc.GetTriggerRequest], trigger.Trigger]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTrigger(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_channel_connections(
        self,
    ) -> Callable[
        [eventarc.ListChannelConnectionsRequest],
        eventarc.ListChannelConnectionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListChannelConnections(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_channels(
        self,
    ) -> Callable[[eventarc.ListChannelsRequest], eventarc.ListChannelsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListChannels(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_providers(
        self,
    ) -> Callable[[eventarc.ListProvidersRequest], eventarc.ListProvidersResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListProviders(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_triggers(
        self,
    ) -> Callable[[eventarc.ListTriggersRequest], eventarc.ListTriggersResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTriggers(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_channel(
        self,
    ) -> Callable[[eventarc.UpdateChannelRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateChannel(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_google_channel_config(
        self,
    ) -> Callable[
        [eventarc.UpdateGoogleChannelConfigRequest],
        gce_google_channel_config.GoogleChannelConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateGoogleChannelConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_trigger(
        self,
    ) -> Callable[[eventarc.UpdateTriggerRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateTrigger(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_location(self):
        return self._GetLocation(self._session, self._host, self._interceptor)  # type: ignore

    class _GetLocation(_BaseEventarcRestTransport._BaseGetLocation, EventarcRestStub):
        def __hash__(self):
            return hash("EventarcRestTransport.GetLocation")

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
                _BaseEventarcRestTransport._BaseGetLocation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_location(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseGetLocation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseGetLocation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._GetLocation._get_response(
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
        _BaseEventarcRestTransport._BaseListLocations, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.ListLocations")

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
                _BaseEventarcRestTransport._BaseListLocations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_locations(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseListLocations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseListLocations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._ListLocations._get_response(
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
    def get_iam_policy(self):
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _GetIamPolicy(_BaseEventarcRestTransport._BaseGetIamPolicy, EventarcRestStub):
        def __hash__(self):
            return hash("EventarcRestTransport.GetIamPolicy")

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

            http_options = (
                _BaseEventarcRestTransport._BaseGetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseGetIamPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseGetIamPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._GetIamPolicy._get_response(
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
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    @property
    def set_iam_policy(self):
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    class _SetIamPolicy(_BaseEventarcRestTransport._BaseSetIamPolicy, EventarcRestStub):
        def __hash__(self):
            return hash("EventarcRestTransport.SetIamPolicy")

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

            http_options = (
                _BaseEventarcRestTransport._BaseSetIamPolicy._get_http_options()
            )
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseSetIamPolicy._get_transcoded_request(
                    http_options, request
                )
            )

            body = _BaseEventarcRestTransport._BaseSetIamPolicy._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseSetIamPolicy._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._SetIamPolicy._get_response(
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

            content = response.content.decode("utf-8")
            resp = policy_pb2.Policy()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    @property
    def test_iam_permissions(self):
        return self._TestIamPermissions(self._session, self._host, self._interceptor)  # type: ignore

    class _TestIamPermissions(
        _BaseEventarcRestTransport._BaseTestIamPermissions, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.TestIamPermissions")

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

            http_options = (
                _BaseEventarcRestTransport._BaseTestIamPermissions._get_http_options()
            )
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            transcoded_request = _BaseEventarcRestTransport._BaseTestIamPermissions._get_transcoded_request(
                http_options, request
            )

            body = _BaseEventarcRestTransport._BaseTestIamPermissions._get_request_body_json(
                transcoded_request
            )

            # Jsonify the query params
            query_params = _BaseEventarcRestTransport._BaseTestIamPermissions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = EventarcRestTransport._TestIamPermissions._get_response(
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

            content = response.content.decode("utf-8")
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            resp = json_format.Parse(content, resp)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(
        _BaseEventarcRestTransport._BaseCancelOperation, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.CancelOperation")

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
                _BaseEventarcRestTransport._BaseCancelOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_cancel_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseEventarcRestTransport._BaseCancelOperation._get_transcoded_request(
                    http_options, request
                )
            )

            body = (
                _BaseEventarcRestTransport._BaseCancelOperation._get_request_body_json(
                    transcoded_request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseCancelOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._CancelOperation._get_response(
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
        _BaseEventarcRestTransport._BaseDeleteOperation, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.DeleteOperation")

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
                _BaseEventarcRestTransport._BaseDeleteOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_delete_operation(
                request, metadata
            )
            transcoded_request = (
                _BaseEventarcRestTransport._BaseDeleteOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseDeleteOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._DeleteOperation._get_response(
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

    class _GetOperation(_BaseEventarcRestTransport._BaseGetOperation, EventarcRestStub):
        def __hash__(self):
            return hash("EventarcRestTransport.GetOperation")

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
                _BaseEventarcRestTransport._BaseGetOperation._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_operation(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseGetOperation._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseGetOperation._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._GetOperation._get_response(
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
        _BaseEventarcRestTransport._BaseListOperations, EventarcRestStub
    ):
        def __hash__(self):
            return hash("EventarcRestTransport.ListOperations")

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
                _BaseEventarcRestTransport._BaseListOperations._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_operations(request, metadata)
            transcoded_request = (
                _BaseEventarcRestTransport._BaseListOperations._get_transcoded_request(
                    http_options, request
                )
            )

            # Jsonify the query params
            query_params = (
                _BaseEventarcRestTransport._BaseListOperations._get_query_params_json(
                    transcoded_request
                )
            )

            # Send the request
            response = EventarcRestTransport._ListOperations._get_response(
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


__all__ = ("EventarcRestTransport",)
