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

from google.cloud.monitoring_v3.proto import service_service_pb2_grpc


class ServiceMonitoringServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.monitoring.v3 ServiceMonitoringService API.

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
            "service_monitoring_service_stub": service_service_pb2_grpc.ServiceMonitoringServiceStub(
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
    def create_service(self):
        """Return the gRPC stub for :meth:`ServiceMonitoringServiceClient.create_service`.

        Create a ``Service``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["service_monitoring_service_stub"].CreateService

    @property
    def get_service(self):
        """Return the gRPC stub for :meth:`ServiceMonitoringServiceClient.get_service`.

        Get the named ``Service``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["service_monitoring_service_stub"].GetService

    @property
    def list_services(self):
        """Return the gRPC stub for :meth:`ServiceMonitoringServiceClient.list_services`.

        List ``Service``\ s for this workspace.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["service_monitoring_service_stub"].ListServices

    @property
    def update_service(self):
        """Return the gRPC stub for :meth:`ServiceMonitoringServiceClient.update_service`.

        Update this ``Service``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["service_monitoring_service_stub"].UpdateService

    @property
    def delete_service(self):
        """Return the gRPC stub for :meth:`ServiceMonitoringServiceClient.delete_service`.

        Soft delete this ``Service``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["service_monitoring_service_stub"].DeleteService

    @property
    def create_service_level_objective(self):
        """Return the gRPC stub for :meth:`ServiceMonitoringServiceClient.create_service_level_objective`.

        Create a ``ServiceLevelObjective`` for the given ``Service``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            "service_monitoring_service_stub"
        ].CreateServiceLevelObjective

    @property
    def get_service_level_objective(self):
        """Return the gRPC stub for :meth:`ServiceMonitoringServiceClient.get_service_level_objective`.

        Get a ``ServiceLevelObjective`` by name.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["service_monitoring_service_stub"].GetServiceLevelObjective

    @property
    def list_service_level_objectives(self):
        """Return the gRPC stub for :meth:`ServiceMonitoringServiceClient.list_service_level_objectives`.

        List the ``ServiceLevelObjective``\ s for the given ``Service``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["service_monitoring_service_stub"].ListServiceLevelObjectives

    @property
    def update_service_level_objective(self):
        """Return the gRPC stub for :meth:`ServiceMonitoringServiceClient.update_service_level_objective`.

        Update the given ``ServiceLevelObjective``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            "service_monitoring_service_stub"
        ].UpdateServiceLevelObjective

    @property
    def delete_service_level_objective(self):
        """Return the gRPC stub for :meth:`ServiceMonitoringServiceClient.delete_service_level_objective`.

        Delete the given ``ServiceLevelObjective``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs[
            "service_monitoring_service_stub"
        ].DeleteServiceLevelObjective
