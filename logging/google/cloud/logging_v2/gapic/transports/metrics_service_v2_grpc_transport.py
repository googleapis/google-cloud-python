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

from google.cloud.logging_v2.proto import logging_metrics_pb2_grpc


class MetricsServiceV2GrpcTransport(object):
    """gRPC transport class providing stubs for
    google.logging.v2 MetricsServiceV2 API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
        "https://www.googleapis.com/auth/logging.admin",
        "https://www.googleapis.com/auth/logging.read",
        "https://www.googleapis.com/auth/logging.write",
    )

    def __init__(
        self, channel=None, credentials=None, address="logging.googleapis.com:443"
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
            "metrics_service_v2_stub": logging_metrics_pb2_grpc.MetricsServiceV2Stub(
                channel
            )
        }

    @classmethod
    def create_channel(cls, address="logging.googleapis.com:443", credentials=None):
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
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_log_metrics(self):
        """Return the gRPC stub for :meth:`MetricsServiceV2Client.list_log_metrics`.

        Lists logs-based metrics.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metrics_service_v2_stub"].ListLogMetrics

    @property
    def get_log_metric(self):
        """Return the gRPC stub for :meth:`MetricsServiceV2Client.get_log_metric`.

        Gets a logs-based metric.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metrics_service_v2_stub"].GetLogMetric

    @property
    def create_log_metric(self):
        """Return the gRPC stub for :meth:`MetricsServiceV2Client.create_log_metric`.

        Creates a logs-based metric.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metrics_service_v2_stub"].CreateLogMetric

    @property
    def update_log_metric(self):
        """Return the gRPC stub for :meth:`MetricsServiceV2Client.update_log_metric`.

        Creates or updates a logs-based metric.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metrics_service_v2_stub"].UpdateLogMetric

    @property
    def delete_log_metric(self):
        """Return the gRPC stub for :meth:`MetricsServiceV2Client.delete_log_metric`.

        Deletes a logs-based metric.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metrics_service_v2_stub"].DeleteLogMetric
