# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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

from google.cloud.monitoring_v3.proto import uptime_service_pb2_grpc


class UptimeCheckServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.monitoring.v3 UptimeCheckService API.

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
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "uptime_check_service_stub": uptime_service_pb2_grpc.UptimeCheckServiceStub(
                channel
            )
        }

    @classmethod
    def create_channel(
        cls, address="monitoring.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_uptime_check_configs(self):
        """Return the gRPC stub for :meth:`UptimeCheckServiceClient.list_uptime_check_configs`.

        Lists the existing valid Uptime check configurations for the project
        (leaving out any invalid configurations).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["uptime_check_service_stub"].ListUptimeCheckConfigs

    @property
    def get_uptime_check_config(self):
        """Return the gRPC stub for :meth:`UptimeCheckServiceClient.get_uptime_check_config`.

        Gets a single Uptime check configuration.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["uptime_check_service_stub"].GetUptimeCheckConfig

    @property
    def create_uptime_check_config(self):
        """Return the gRPC stub for :meth:`UptimeCheckServiceClient.create_uptime_check_config`.

        Creates a new Uptime check configuration.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["uptime_check_service_stub"].CreateUptimeCheckConfig

    @property
    def update_uptime_check_config(self):
        """Return the gRPC stub for :meth:`UptimeCheckServiceClient.update_uptime_check_config`.

        Updates an Uptime check configuration. You can either replace the
        entire configuration with a new one or replace only certain fields in
        the current configuration by specifying the fields to be updated via
        ``updateMask``. Returns the updated configuration.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["uptime_check_service_stub"].UpdateUptimeCheckConfig

    @property
    def delete_uptime_check_config(self):
        """Return the gRPC stub for :meth:`UptimeCheckServiceClient.delete_uptime_check_config`.

        Deletes an Uptime check configuration. Note that this method will fail
        if the Uptime check configuration is referenced by an alert policy or
        other dependent configs that would be rendered invalid by the deletion.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["uptime_check_service_stub"].DeleteUptimeCheckConfig

    @property
    def list_uptime_check_ips(self):
        """Return the gRPC stub for :meth:`UptimeCheckServiceClient.list_uptime_check_ips`.

        Returns the list of IP addresses that checkers run from

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["uptime_check_service_stub"].ListUptimeCheckIps
