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

from google.cloud.monitoring_v3.proto import metric_service_pb2_grpc


class MetricServiceGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.monitoring.v3 MetricService API.

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
            "metric_service_stub": metric_service_pb2_grpc.MetricServiceStub(channel)
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
    def list_monitored_resource_descriptors(self):
        """Return the gRPC stub for :meth:`MetricServiceClient.list_monitored_resource_descriptors`.

        Lists monitored resource descriptors that match a filter. This method does not require a Stackdriver account.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metric_service_stub"].ListMonitoredResourceDescriptors

    @property
    def get_monitored_resource_descriptor(self):
        """Return the gRPC stub for :meth:`MetricServiceClient.get_monitored_resource_descriptor`.

        Gets a single monitored resource descriptor. This method does not require a Stackdriver account.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metric_service_stub"].GetMonitoredResourceDescriptor

    @property
    def list_metric_descriptors(self):
        """Return the gRPC stub for :meth:`MetricServiceClient.list_metric_descriptors`.

        Lists metric descriptors that match a filter. This method does not require a Stackdriver account.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metric_service_stub"].ListMetricDescriptors

    @property
    def get_metric_descriptor(self):
        """Return the gRPC stub for :meth:`MetricServiceClient.get_metric_descriptor`.

        Gets a single metric descriptor. This method does not require a Stackdriver account.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metric_service_stub"].GetMetricDescriptor

    @property
    def create_metric_descriptor(self):
        """Return the gRPC stub for :meth:`MetricServiceClient.create_metric_descriptor`.

        Creates a new metric descriptor. User-created metric descriptors define
        `custom metrics <https://cloud.google.com/monitoring/custom-metrics>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metric_service_stub"].CreateMetricDescriptor

    @property
    def delete_metric_descriptor(self):
        """Return the gRPC stub for :meth:`MetricServiceClient.delete_metric_descriptor`.

        Deletes a metric descriptor. Only user-created `custom
        metrics <https://cloud.google.com/monitoring/custom-metrics>`__ can be
        deleted.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metric_service_stub"].DeleteMetricDescriptor

    @property
    def list_time_series(self):
        """Return the gRPC stub for :meth:`MetricServiceClient.list_time_series`.

        Lists time series that match a filter. This method does not require a Stackdriver account.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metric_service_stub"].ListTimeSeries

    @property
    def create_time_series(self):
        """Return the gRPC stub for :meth:`MetricServiceClient.create_time_series`.

        Creates or adds data to one or more time series.
        The response is empty if all time series in the request were written.
        If any time series could not be written, a corresponding failure message is
        included in the error response.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["metric_service_stub"].CreateTimeSeries
