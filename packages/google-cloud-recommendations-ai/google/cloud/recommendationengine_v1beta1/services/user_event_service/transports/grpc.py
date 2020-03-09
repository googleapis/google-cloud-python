# -*- coding: utf-8 -*-

# Copyright (C) 2019  Google LLC
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

from typing import Callable, Dict

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore

import grpc  # type: ignore

from google.api import httpbody_pb2 as httpbody  # type: ignore
from google.cloud.recommendationengine_v1beta1.types import import_
from google.cloud.recommendationengine_v1beta1.types import user_event
from google.cloud.recommendationengine_v1beta1.types import user_event_service
from google.longrunning import operations_pb2 as operations  # type: ignore

from .base import UserEventServiceTransport


class UserEventServiceGrpcTransport(UserEventServiceTransport):
    """gRPC backend transport for UserEventService.

    Service for ingesting end user actions on the customer
    website.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    def __init__(
        self,
        *,
        host: str = "recommendationengine.googleapis.com",
        credentials: credentials.Credentials = None,
        channel: grpc.Channel = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
        """
        # Sanity check: Ensure that channel and credentials are not both
        # provided.
        if channel:
            credentials = False

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

        # If a channel was explicitly provided, set it.
        if channel:
            self._grpc_channel = channel

    @classmethod
    def create_channel(
        cls,
        host: str = "recommendationengine.googleapis.com",
        credentials: credentials.Credentials = None,
        **kwargs
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return grpc_helpers.create_channel(
            host, credentials=credentials, scopes=cls.AUTH_SCOPES, **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def write_user_event(
        self
    ) -> Callable[[user_event_service.WriteUserEventRequest], user_event.UserEvent]:
        r"""Return a callable for the write user event method over gRPC.

        Writes a single user event.

        Returns:
            Callable[[~.WriteUserEventRequest],
                    ~.UserEvent]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "write_user_event" not in self._stubs:
            self._stubs["write_user_event"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.UserEventService/WriteUserEvent",
                request_serializer=user_event_service.WriteUserEventRequest.serialize,
                response_deserializer=user_event.UserEvent.deserialize,
            )
        return self._stubs["write_user_event"]

    @property
    def collect_user_event(
        self
    ) -> Callable[[user_event_service.CollectUserEventRequest], httpbody.HttpBody]:
        r"""Return a callable for the collect user event method over gRPC.

        Writes a single user event from the browser. This
        uses a GET request to due to browser restriction of
        POST-ing to a 3rd party domain.
        This method is used only by the Recommendations AI
        JavaScript pixel. Users should not call this method
        directly.

        Returns:
            Callable[[~.CollectUserEventRequest],
                    ~.HttpBody]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "collect_user_event" not in self._stubs:
            self._stubs["collect_user_event"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.UserEventService/CollectUserEvent",
                request_serializer=user_event_service.CollectUserEventRequest.serialize,
                response_deserializer=httpbody.HttpBody.FromString,
            )
        return self._stubs["collect_user_event"]

    @property
    def list_user_events(
        self
    ) -> Callable[
        [user_event_service.ListUserEventsRequest],
        user_event_service.ListUserEventsResponse,
    ]:
        r"""Return a callable for the list user events method over gRPC.

        Gets a list of user events within a time range, with
        potential filtering.

        Returns:
            Callable[[~.ListUserEventsRequest],
                    ~.ListUserEventsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_user_events" not in self._stubs:
            self._stubs["list_user_events"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.UserEventService/ListUserEvents",
                request_serializer=user_event_service.ListUserEventsRequest.serialize,
                response_deserializer=user_event_service.ListUserEventsResponse.deserialize,
            )
        return self._stubs["list_user_events"]

    @property
    def purge_user_events(
        self
    ) -> Callable[[user_event_service.PurgeUserEventsRequest], operations.Operation]:
        r"""Return a callable for the purge user events method over gRPC.

        Deletes permanently all user events specified by the
        filter provided. Depending on the number of events
        specified by the filter, this operation could take hours
        or days to complete. To test a filter, use the list
        command first.

        Returns:
            Callable[[~.PurgeUserEventsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "purge_user_events" not in self._stubs:
            self._stubs["purge_user_events"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.UserEventService/PurgeUserEvents",
                request_serializer=user_event_service.PurgeUserEventsRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["purge_user_events"]

    @property
    def import_user_events(
        self
    ) -> Callable[[import_.ImportUserEventsRequest], operations.Operation]:
        r"""Return a callable for the import user events method over gRPC.

        Bulk import of User events. Request processing might
        be synchronous. Events that already exist are skipped.
        Use this method for backfilling historical user events.
        Operation.response is of type ImportResponse. Note that
        it is possible for a subset of the items to be
        successfully inserted. Operation.metadata is of type
        ImportMetadata.

        Returns:
            Callable[[~.ImportUserEventsRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_user_events" not in self._stubs:
            self._stubs["import_user_events"] = self.grpc_channel.unary_unary(
                "/google.cloud.recommendationengine.v1beta1.UserEventService/ImportUserEvents",
                request_serializer=import_.ImportUserEventsRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["import_user_events"]


__all__ = ("UserEventServiceGrpcTransport",)
