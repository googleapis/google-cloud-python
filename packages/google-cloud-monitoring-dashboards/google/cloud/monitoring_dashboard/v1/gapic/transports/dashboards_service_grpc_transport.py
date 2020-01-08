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

from google.cloud.monitoring_dashboard.v1.proto import dashboards_service_pb2_grpc


class DashboardsServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.monitoring.dashboard.v1 DashboardsService API.

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
            "dashboards_service_stub": dashboards_service_pb2_grpc.DashboardsServiceStub(
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
    def create_dashboard(self):
        """Return the gRPC stub for :meth:`DashboardsServiceClient.create_dashboard`.

        Creates a new custom dashboard.

        This method requires the ``monitoring.dashboards.create`` permission on
        the specified project. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["dashboards_service_stub"].CreateDashboard

    @property
    def list_dashboards(self):
        """Return the gRPC stub for :meth:`DashboardsServiceClient.list_dashboards`.

        Lists the existing dashboards.

        This method requires the ``monitoring.dashboards.list`` permission on
        the specified project. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["dashboards_service_stub"].ListDashboards

    @property
    def get_dashboard(self):
        """Return the gRPC stub for :meth:`DashboardsServiceClient.get_dashboard`.

        Fetches a specific dashboard.

        This method requires the ``monitoring.dashboards.get`` permission on the
        specified dashboard. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["dashboards_service_stub"].GetDashboard

    @property
    def delete_dashboard(self):
        """Return the gRPC stub for :meth:`DashboardsServiceClient.delete_dashboard`.

        Deletes an existing custom dashboard.

        This method requires the ``monitoring.dashboards.delete`` permission on
        the specified dashboard. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["dashboards_service_stub"].DeleteDashboard

    @property
    def update_dashboard(self):
        """Return the gRPC stub for :meth:`DashboardsServiceClient.update_dashboard`.

        Replaces an existing custom dashboard with a new definition.

        This method requires the ``monitoring.dashboards.update`` permission on
        the specified dashboard. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["dashboards_service_stub"].UpdateDashboard
