# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.api_core.grpc_helpers

from google.cloud.monitoring_v3.proto import notification_service_pb2_grpc


class NotificationChannelServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.monitoring.v3 NotificationChannelService API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/monitoring",
        "https://www.googleapis.com/auth/monitoring.read",
        "https://www.googleapis.com/auth/monitoring.write",
    )

    def __init__(
        self, channel=None, credentials=None, address="monitoring.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address=address, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "notification_channel_service_stub": notification_service_pb2_grpc.NotificationChannelServiceStub(
                channel
            )
        }

    @classmethod
    def create_channel(cls, address="monitoring.googleapis.com:443", credentials=None):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address,
            credentials=credentials,
            scopes=cls._OAUTH_SCOPES,
            options={
                "grpc.max_send_message_length": -1,
                "grpc.max_receive_message_length": -1,
            }.items(),
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_notification_channel_descriptors(self):
        """Return the gRPC stub for :meth:`NotificationChannelServiceClient.list_notification_channel_descriptors`.

        Lists the descriptors for supported channel types. The use of descriptors
        makes it possible for new channel types to be dynamically added.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            "notification_channel_service_stub"
        ].ListNotificationChannelDescriptors

    @property
    def get_notification_channel_descriptor(self):
        """Return the gRPC stub for :meth:`NotificationChannelServiceClient.get_notification_channel_descriptor`.

        Gets a single channel descriptor. The descriptor indicates which fields
        are expected / permitted for a notification channel of the given type.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            "notification_channel_service_stub"
        ].GetNotificationChannelDescriptor

    @property
    def list_notification_channels(self):
        """Return the gRPC stub for :meth:`NotificationChannelServiceClient.list_notification_channels`.

        Lists the notification channels that have been created for the project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["notification_channel_service_stub"].ListNotificationChannels

    @property
    def get_notification_channel(self):
        """Return the gRPC stub for :meth:`NotificationChannelServiceClient.get_notification_channel`.

        Gets a single notification channel. The channel includes the relevant
        configuration details with which the channel was created. However, the
        response may truncate or omit passwords, API keys, or other private key
        matter and thus the response may not be 100% identical to the information
        that was supplied in the call to the create method.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["notification_channel_service_stub"].GetNotificationChannel

    @property
    def create_notification_channel(self):
        """Return the gRPC stub for :meth:`NotificationChannelServiceClient.create_notification_channel`.

        Creates a new notification channel, representing a single notification
        endpoint such as an email address, SMS number, or PagerDuty service.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            "notification_channel_service_stub"
        ].CreateNotificationChannel

    @property
    def update_notification_channel(self):
        """Return the gRPC stub for :meth:`NotificationChannelServiceClient.update_notification_channel`.

        Updates a notification channel. Fields not specified in the field mask
        remain unchanged.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            "notification_channel_service_stub"
        ].UpdateNotificationChannel

    @property
    def delete_notification_channel(self):
        """Return the gRPC stub for :meth:`NotificationChannelServiceClient.delete_notification_channel`.

        Deletes a notification channel.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            "notification_channel_service_stub"
        ].DeleteNotificationChannel
