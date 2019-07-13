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

from google.cloud.devtools.containeranalysis_v1.proto import containeranalysis_pb2_grpc


class ContainerAnalysisGrpcTransport(object):
    """gRPC transport class providing stubs for
    google.devtools.containeranalysis.v1 ContainerAnalysis API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        channel=None,
        credentials=None,
        address="containeranalysis.googleapis.com:443",
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
            "container_analysis_stub": containeranalysis_pb2_grpc.ContainerAnalysisStub(
                channel
            )
        }

    @classmethod
    def create_channel(
        cls, address="containeranalysis.googleapis.com:443", credentials=None, **kwargs
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
    def set_iam_policy(self):
        """Return the gRPC stub for :meth:`ContainerAnalysisClient.set_iam_policy`.

        Sets the access control policy on the specified note or occurrence.
        Requires ``containeranalysis.notes.setIamPolicy`` or
        ``containeranalysis.occurrences.setIamPolicy`` permission if the
        resource is a note or an occurrence, respectively.

        The resource takes the format ``projects/[PROJECT_ID]/notes/[NOTE_ID]``
        for notes and ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]`` for
        occurrences.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["container_analysis_stub"].SetIamPolicy

    @property
    def get_iam_policy(self):
        """Return the gRPC stub for :meth:`ContainerAnalysisClient.get_iam_policy`.

        Gets the access control policy for a note or an occurrence resource.
        Requires ``containeranalysis.notes.setIamPolicy`` or
        ``containeranalysis.occurrences.setIamPolicy`` permission if the
        resource is a note or occurrence, respectively.

        The resource takes the format ``projects/[PROJECT_ID]/notes/[NOTE_ID]``
        for notes and ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]`` for
        occurrences.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["container_analysis_stub"].GetIamPolicy

    @property
    def test_iam_permissions(self):
        """Return the gRPC stub for :meth:`ContainerAnalysisClient.test_iam_permissions`.

        Returns the permissions that a caller has on the specified note or
        occurrence. Requires list permission on the project (for example,
        ``containeranalysis.notes.list``).

        The resource takes the format ``projects/[PROJECT_ID]/notes/[NOTE_ID]``
        for notes and ``projects/[PROJECT_ID]/occurrences/[OCCURRENCE_ID]`` for
        occurrences.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["container_analysis_stub"].TestIamPermissions
