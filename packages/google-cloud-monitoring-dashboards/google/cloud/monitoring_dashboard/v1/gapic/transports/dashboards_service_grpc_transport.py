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

        Identifies which part of the FileDescriptorProto was defined at this
        location.

        Each element is a field number or an index. They form a path from the
        root FileDescriptorProto to the place where the definition. For example,
        this path: [ 4, 3, 2, 7, 1 ] refers to: file.message_type(3) // 4, 3
        .field(7) // 2, 7 .name() // 1 This is because
        FileDescriptorProto.message_type has field number 4: repeated
        DescriptorProto message_type = 4; and DescriptorProto.field has field
        number 2: repeated FieldDescriptorProto field = 2; and
        FieldDescriptorProto.name has field number 1: optional string name = 1;

        Thus, the above path gives the location of a field name. If we removed
        the last element: [ 4, 3, 2, 7 ] this path refers to the whole field
        declaration (from the beginning of the label to the terminating
        semicolon).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["dashboards_service_stub"].CreateDashboard

    @property
    def list_dashboards(self):
        """Return the gRPC stub for :meth:`DashboardsServiceClient.list_dashboards`.

        An annotation that describes a resource definition without a
        corresponding message; see ``ResourceDescriptor``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["dashboards_service_stub"].ListDashboards

    @property
    def get_dashboard(self):
        """Return the gRPC stub for :meth:`DashboardsServiceClient.get_dashboard`.

        Align and convert to a percentage change. This alignment is valid
        for gauge and delta metrics with numeric values. This alignment
        conceptually computes the equivalent of "((current -
        previous)/previous)*100" where previous value is determined based on the
        alignmentPeriod. In the event that previous is 0 the calculated value is
        infinity with the exception that if both (current - previous) and
        previous are 0 the calculated value is 0. A 10 minute moving mean is
        computed at each point of the time window prior to the above calculation
        to smooth the metric and prevent false positives from very short lived
        spikes. Only applicable for data that is >= 0. Any values < 0 are
        treated as no data. While delta metrics are accepted by this alignment
        special care should be taken that the values for the metric will always
        be positive. The output is a gauge metric with value type ``DOUBLE``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["dashboards_service_stub"].GetDashboard

    @property
    def delete_dashboard(self):
        """Return the gRPC stub for :meth:`DashboardsServiceClient.delete_dashboard`.

        Protocol Buffers - Google's data interchange format Copyright 2008
        Google Inc. All rights reserved.
        https://developers.google.com/protocol-buffers/

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions are
        met:

        ::

            * Redistributions of source code must retain the above copyright

        notice, this list of conditions and the following disclaimer. \*
        Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution. \*
        Neither the name of Google Inc. nor the names of its contributors may be
        used to endorse or promote products derived from this software without
        specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
        IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
        TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
        PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
        OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
        EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
        PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
        PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
        LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
        NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["dashboards_service_stub"].DeleteDashboard

    @property
    def update_dashboard(self):
        """Return the gRPC stub for :meth:`DashboardsServiceClient.update_dashboard`.

        Deletes an existing custom dashboard.

        This method requires the ``monitoring.dashboards.delete`` permission on
        the specified dashboard. For more information, see `Google Cloud
        IAM <https://cloud.google.com/iam>`__.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["dashboards_service_stub"].UpdateDashboard
