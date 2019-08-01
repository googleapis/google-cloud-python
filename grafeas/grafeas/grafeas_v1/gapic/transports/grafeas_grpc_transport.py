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

from grafeas.grafeas_v1.proto import grafeas_pb2_grpc


class GrafeasGrpcTransport(object):
    """gRPC transport class providing stubs for
    grafeas.v1 Grafeas API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    def __init__(self, address, scopes, channel=None, credentials=None):
        """Instantiate the transport class.

        Args:
            address (str): The address where the service is hosted.
            scopes (Sequence[str]): The scopes needed to make gRPC calls.
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive."
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(address, scopes, credentials=credentials)

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {"grafeas_stub": grafeas_pb2_grpc.GrafeasStub(channel)}

    @classmethod
    def create_channel(cls, address, scopes, credentials=None, **kwargs):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            scopes (Sequence[str]): The scopes needed to make gRPC calls.
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
            address, credentials=credentials, scopes=scopes, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def get_occurrence(self):
        """Return the gRPC stub for :meth:`GrafeasClient.get_occurrence`.

        Gets the specified occurrence.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].GetOccurrence

    @property
    def list_occurrences(self):
        """Return the gRPC stub for :meth:`GrafeasClient.list_occurrences`.

        Lists occurrences for the specified project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].ListOccurrences

    @property
    def delete_occurrence(self):
        """Return the gRPC stub for :meth:`GrafeasClient.delete_occurrence`.

        Deletes the specified occurrence. For example, use this method to delete an
        occurrence when the occurrence is no longer applicable for the given
        resource.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].DeleteOccurrence

    @property
    def create_occurrence(self):
        """Return the gRPC stub for :meth:`GrafeasClient.create_occurrence`.

        Creates a new occurrence.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].CreateOccurrence

    @property
    def batch_create_occurrences(self):
        """Return the gRPC stub for :meth:`GrafeasClient.batch_create_occurrences`.

        Creates new occurrences in batch.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].BatchCreateOccurrences

    @property
    def update_occurrence(self):
        """Return the gRPC stub for :meth:`GrafeasClient.update_occurrence`.

        Updates the specified occurrence.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].UpdateOccurrence

    @property
    def get_occurrence_note(self):
        """Return the gRPC stub for :meth:`GrafeasClient.get_occurrence_note`.

        Gets the note attached to the specified occurrence. Consumer projects can
        use this method to get a note that belongs to a provider project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].GetOccurrenceNote

    @property
    def get_note(self):
        """Return the gRPC stub for :meth:`GrafeasClient.get_note`.

        Gets the specified note.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].GetNote

    @property
    def list_notes(self):
        """Return the gRPC stub for :meth:`GrafeasClient.list_notes`.

        Lists notes for the specified project.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].ListNotes

    @property
    def delete_note(self):
        """Return the gRPC stub for :meth:`GrafeasClient.delete_note`.

        Deletes the specified note.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].DeleteNote

    @property
    def create_note(self):
        """Return the gRPC stub for :meth:`GrafeasClient.create_note`.

        Creates a new note.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].CreateNote

    @property
    def batch_create_notes(self):
        """Return the gRPC stub for :meth:`GrafeasClient.batch_create_notes`.

        Creates new notes in batch.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].BatchCreateNotes

    @property
    def update_note(self):
        """Return the gRPC stub for :meth:`GrafeasClient.update_note`.

        Updates the specified note.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].UpdateNote

    @property
    def list_note_occurrences(self):
        """Return the gRPC stub for :meth:`GrafeasClient.list_note_occurrences`.

        Lists occurrences referencing the specified note. Provider projects can use
        this method to get all occurrences across consumer projects referencing the
        specified note.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["grafeas_stub"].ListNoteOccurrences
