# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers_async  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.protobuf import empty_pb2 as empty  # type: ignore
from grafeas.grafeas_v1.types import grafeas

from .base import GrafeasTransport
from .grpc import GrafeasGrpcTransport


class GrafeasGrpcAsyncIOTransport(GrafeasTransport):
    """gRPC AsyncIO backend transport for Grafeas.

    `Grafeas <https://grafeas.io>`__ API.

    Retrieves analysis results of Cloud components such as Docker
    container images.

    Analysis results are stored as a series of occurrences. An
    ``Occurrence`` contains information about a specific analysis
    instance on a resource. An occurrence refers to a ``Note``. A note
    contains details describing the analysis and is generally stored in
    a separate project, called a ``Provider``. Multiple occurrences can
    refer to the same note.

    For example, an SSL vulnerability could affect multiple images. In
    this case, there would be one note for the vulnerability and an
    occurrence for each image with the vulnerability referring to that
    note.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
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
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
        )

        self._stubs = {}

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def get_occurrence(
        self,
    ) -> Callable[[grafeas.GetOccurrenceRequest], Awaitable[grafeas.Occurrence]]:
        r"""Return a callable for the get occurrence method over gRPC.

        Gets the specified occurrence.

        Returns:
            Callable[[~.GetOccurrenceRequest],
                    Awaitable[~.Occurrence]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_occurrence" not in self._stubs:
            self._stubs["get_occurrence"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/GetOccurrence",
                request_serializer=grafeas.GetOccurrenceRequest.serialize,
                response_deserializer=grafeas.Occurrence.deserialize,
            )
        return self._stubs["get_occurrence"]

    @property
    def list_occurrences(
        self,
    ) -> Callable[
        [grafeas.ListOccurrencesRequest], Awaitable[grafeas.ListOccurrencesResponse]
    ]:
        r"""Return a callable for the list occurrences method over gRPC.

        Lists occurrences for the specified project.

        Returns:
            Callable[[~.ListOccurrencesRequest],
                    Awaitable[~.ListOccurrencesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_occurrences" not in self._stubs:
            self._stubs["list_occurrences"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/ListOccurrences",
                request_serializer=grafeas.ListOccurrencesRequest.serialize,
                response_deserializer=grafeas.ListOccurrencesResponse.deserialize,
            )
        return self._stubs["list_occurrences"]

    @property
    def delete_occurrence(
        self,
    ) -> Callable[[grafeas.DeleteOccurrenceRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete occurrence method over gRPC.

        Deletes the specified occurrence. For example, use
        this method to delete an occurrence when the occurrence
        is no longer applicable for the given resource.

        Returns:
            Callable[[~.DeleteOccurrenceRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_occurrence" not in self._stubs:
            self._stubs["delete_occurrence"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/DeleteOccurrence",
                request_serializer=grafeas.DeleteOccurrenceRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_occurrence"]

    @property
    def create_occurrence(
        self,
    ) -> Callable[[grafeas.CreateOccurrenceRequest], Awaitable[grafeas.Occurrence]]:
        r"""Return a callable for the create occurrence method over gRPC.

        Creates a new occurrence.

        Returns:
            Callable[[~.CreateOccurrenceRequest],
                    Awaitable[~.Occurrence]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_occurrence" not in self._stubs:
            self._stubs["create_occurrence"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/CreateOccurrence",
                request_serializer=grafeas.CreateOccurrenceRequest.serialize,
                response_deserializer=grafeas.Occurrence.deserialize,
            )
        return self._stubs["create_occurrence"]

    @property
    def batch_create_occurrences(
        self,
    ) -> Callable[
        [grafeas.BatchCreateOccurrencesRequest],
        Awaitable[grafeas.BatchCreateOccurrencesResponse],
    ]:
        r"""Return a callable for the batch create occurrences method over gRPC.

        Creates new occurrences in batch.

        Returns:
            Callable[[~.BatchCreateOccurrencesRequest],
                    Awaitable[~.BatchCreateOccurrencesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_create_occurrences" not in self._stubs:
            self._stubs["batch_create_occurrences"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/BatchCreateOccurrences",
                request_serializer=grafeas.BatchCreateOccurrencesRequest.serialize,
                response_deserializer=grafeas.BatchCreateOccurrencesResponse.deserialize,
            )
        return self._stubs["batch_create_occurrences"]

    @property
    def update_occurrence(
        self,
    ) -> Callable[[grafeas.UpdateOccurrenceRequest], Awaitable[grafeas.Occurrence]]:
        r"""Return a callable for the update occurrence method over gRPC.

        Updates the specified occurrence.

        Returns:
            Callable[[~.UpdateOccurrenceRequest],
                    Awaitable[~.Occurrence]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_occurrence" not in self._stubs:
            self._stubs["update_occurrence"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/UpdateOccurrence",
                request_serializer=grafeas.UpdateOccurrenceRequest.serialize,
                response_deserializer=grafeas.Occurrence.deserialize,
            )
        return self._stubs["update_occurrence"]

    @property
    def get_occurrence_note(
        self,
    ) -> Callable[[grafeas.GetOccurrenceNoteRequest], Awaitable[grafeas.Note]]:
        r"""Return a callable for the get occurrence note method over gRPC.

        Gets the note attached to the specified occurrence.
        Consumer projects can use this method to get a note that
        belongs to a provider project.

        Returns:
            Callable[[~.GetOccurrenceNoteRequest],
                    Awaitable[~.Note]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_occurrence_note" not in self._stubs:
            self._stubs["get_occurrence_note"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/GetOccurrenceNote",
                request_serializer=grafeas.GetOccurrenceNoteRequest.serialize,
                response_deserializer=grafeas.Note.deserialize,
            )
        return self._stubs["get_occurrence_note"]

    @property
    def get_note(self) -> Callable[[grafeas.GetNoteRequest], Awaitable[grafeas.Note]]:
        r"""Return a callable for the get note method over gRPC.

        Gets the specified note.

        Returns:
            Callable[[~.GetNoteRequest],
                    Awaitable[~.Note]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_note" not in self._stubs:
            self._stubs["get_note"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/GetNote",
                request_serializer=grafeas.GetNoteRequest.serialize,
                response_deserializer=grafeas.Note.deserialize,
            )
        return self._stubs["get_note"]

    @property
    def list_notes(
        self,
    ) -> Callable[[grafeas.ListNotesRequest], Awaitable[grafeas.ListNotesResponse]]:
        r"""Return a callable for the list notes method over gRPC.

        Lists notes for the specified project.

        Returns:
            Callable[[~.ListNotesRequest],
                    Awaitable[~.ListNotesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_notes" not in self._stubs:
            self._stubs["list_notes"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/ListNotes",
                request_serializer=grafeas.ListNotesRequest.serialize,
                response_deserializer=grafeas.ListNotesResponse.deserialize,
            )
        return self._stubs["list_notes"]

    @property
    def delete_note(
        self,
    ) -> Callable[[grafeas.DeleteNoteRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete note method over gRPC.

        Deletes the specified note.

        Returns:
            Callable[[~.DeleteNoteRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_note" not in self._stubs:
            self._stubs["delete_note"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/DeleteNote",
                request_serializer=grafeas.DeleteNoteRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_note"]

    @property
    def create_note(
        self,
    ) -> Callable[[grafeas.CreateNoteRequest], Awaitable[grafeas.Note]]:
        r"""Return a callable for the create note method over gRPC.

        Creates a new note.

        Returns:
            Callable[[~.CreateNoteRequest],
                    Awaitable[~.Note]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_note" not in self._stubs:
            self._stubs["create_note"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/CreateNote",
                request_serializer=grafeas.CreateNoteRequest.serialize,
                response_deserializer=grafeas.Note.deserialize,
            )
        return self._stubs["create_note"]

    @property
    def batch_create_notes(
        self,
    ) -> Callable[
        [grafeas.BatchCreateNotesRequest], Awaitable[grafeas.BatchCreateNotesResponse]
    ]:
        r"""Return a callable for the batch create notes method over gRPC.

        Creates new notes in batch.

        Returns:
            Callable[[~.BatchCreateNotesRequest],
                    Awaitable[~.BatchCreateNotesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_create_notes" not in self._stubs:
            self._stubs["batch_create_notes"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/BatchCreateNotes",
                request_serializer=grafeas.BatchCreateNotesRequest.serialize,
                response_deserializer=grafeas.BatchCreateNotesResponse.deserialize,
            )
        return self._stubs["batch_create_notes"]

    @property
    def update_note(
        self,
    ) -> Callable[[grafeas.UpdateNoteRequest], Awaitable[grafeas.Note]]:
        r"""Return a callable for the update note method over gRPC.

        Updates the specified note.

        Returns:
            Callable[[~.UpdateNoteRequest],
                    Awaitable[~.Note]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_note" not in self._stubs:
            self._stubs["update_note"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/UpdateNote",
                request_serializer=grafeas.UpdateNoteRequest.serialize,
                response_deserializer=grafeas.Note.deserialize,
            )
        return self._stubs["update_note"]

    @property
    def list_note_occurrences(
        self,
    ) -> Callable[
        [grafeas.ListNoteOccurrencesRequest],
        Awaitable[grafeas.ListNoteOccurrencesResponse],
    ]:
        r"""Return a callable for the list note occurrences method over gRPC.

        Lists occurrences referencing the specified note.
        Provider projects can use this method to get all
        occurrences across consumer projects referencing the
        specified note.

        Returns:
            Callable[[~.ListNoteOccurrencesRequest],
                    Awaitable[~.ListNoteOccurrencesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_note_occurrences" not in self._stubs:
            self._stubs["list_note_occurrences"] = self.grpc_channel.unary_unary(
                "/grafeas.v1.Grafeas/ListNoteOccurrences",
                request_serializer=grafeas.ListNoteOccurrencesRequest.serialize,
                response_deserializer=grafeas.ListNoteOccurrencesResponse.deserialize,
            )
        return self._stubs["list_note_occurrences"]


__all__ = ("GrafeasGrpcAsyncIOTransport",)
