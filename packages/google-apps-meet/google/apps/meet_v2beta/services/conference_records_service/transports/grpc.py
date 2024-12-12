# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
import json
import logging as std_logging
import pickle
from typing import Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers
import google.auth  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.protobuf.json_format import MessageToJson
import google.protobuf.message
import grpc  # type: ignore
import proto  # type: ignore

from google.apps.meet_v2beta.types import resource, service

from .base import DEFAULT_CLIENT_INFO, ConferenceRecordsServiceTransport

try:
    from google.api_core import client_logging  # type: ignore

    CLIENT_LOGGING_SUPPORTED = True  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    CLIENT_LOGGING_SUPPORTED = False

_LOGGER = std_logging.getLogger(__name__)


class _LoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):  # pragma: NO COVER
    def intercept_unary_unary(self, continuation, client_call_details, request):
        logging_enabled = CLIENT_LOGGING_SUPPORTED and _LOGGER.isEnabledFor(
            std_logging.DEBUG
        )
        if logging_enabled:  # pragma: NO COVER
            request_metadata = client_call_details.metadata
            if isinstance(request, proto.Message):
                request_payload = type(request).to_json(request)
            elif isinstance(request, google.protobuf.message.Message):
                request_payload = MessageToJson(request)
            else:
                request_payload = f"{type(request).__name__}: {pickle.dumps(request)}"

            request_metadata = {
                key: value.decode("utf-8") if isinstance(value, bytes) else value
                for key, value in request_metadata
            }
            grpc_request = {
                "payload": request_payload,
                "requestMethod": "grpc",
                "metadata": dict(request_metadata),
            }
            _LOGGER.debug(
                f"Sending request for {client_call_details.method}",
                extra={
                    "serviceName": "google.apps.meet.v2beta.ConferenceRecordsService",
                    "rpcName": client_call_details.method,
                    "request": grpc_request,
                    "metadata": grpc_request["metadata"],
                },
            )

        response = continuation(client_call_details, request)
        if logging_enabled:  # pragma: NO COVER
            response_metadata = response.trailing_metadata()
            # Convert gRPC metadata `<class 'grpc.aio._metadata.Metadata'>` to list of tuples
            metadata = (
                dict([(k, str(v)) for k, v in response_metadata])
                if response_metadata
                else None
            )
            result = response.result()
            if isinstance(result, proto.Message):
                response_payload = type(result).to_json(result)
            elif isinstance(result, google.protobuf.message.Message):
                response_payload = MessageToJson(result)
            else:
                response_payload = f"{type(result).__name__}: {pickle.dumps(result)}"
            grpc_response = {
                "payload": response_payload,
                "metadata": metadata,
                "status": "OK",
            }
            _LOGGER.debug(
                f"Received response for {client_call_details.method}.",
                extra={
                    "serviceName": "google.apps.meet.v2beta.ConferenceRecordsService",
                    "rpcName": client_call_details.method,
                    "response": grpc_response,
                    "metadata": grpc_response["metadata"],
                },
            )
        return response


class ConferenceRecordsServiceGrpcTransport(ConferenceRecordsServiceTransport):
    """gRPC backend transport for ConferenceRecordsService.

    REST API for services dealing with conference records.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "meet.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'meet.googleapis.com').
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if a ``channel`` instance is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if a ``channel`` instance is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if a ``channel`` instance is provided.
            channel (Optional[Union[grpc.Channel, Callable[..., grpc.Channel]]]):
                A ``Channel`` instance through which to make calls, or a Callable
                that constructs and returns one. If set to None, ``self.create_channel``
                is used to create the channel. If a Callable is given, it will be called
                with the same arguments as used in ``self.create_channel``.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if a ``channel`` instance is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if a ``channel`` instance or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if isinstance(channel, grpc.Channel):
            # Ignore credentials if a channel was passed.
            credentials = None
            self._ignore_credentials = True
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            # initialize with the provided callable or the default channel
            channel_init = channel or type(self).create_channel
            self._grpc_channel = channel_init(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        self._interceptor = _LoggingClientInterceptor()
        self._logged_channel = grpc.intercept_channel(
            self._grpc_channel, self._interceptor
        )

        # Wrap messages. This must be done after self._logged_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(
        cls,
        host: str = "meet.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service."""
        return self._grpc_channel

    @property
    def get_conference_record(
        self,
    ) -> Callable[[service.GetConferenceRecordRequest], resource.ConferenceRecord]:
        r"""Return a callable for the get conference record method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a conference record by conference ID.

        Returns:
            Callable[[~.GetConferenceRecordRequest],
                    ~.ConferenceRecord]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_conference_record" not in self._stubs:
            self._stubs["get_conference_record"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/GetConferenceRecord",
                request_serializer=service.GetConferenceRecordRequest.serialize,
                response_deserializer=resource.ConferenceRecord.deserialize,
            )
        return self._stubs["get_conference_record"]

    @property
    def list_conference_records(
        self,
    ) -> Callable[
        [service.ListConferenceRecordsRequest], service.ListConferenceRecordsResponse
    ]:
        r"""Return a callable for the list conference records method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the conference records by start time and in descending
        order.

        Returns:
            Callable[[~.ListConferenceRecordsRequest],
                    ~.ListConferenceRecordsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_conference_records" not in self._stubs:
            self._stubs["list_conference_records"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/ListConferenceRecords",
                request_serializer=service.ListConferenceRecordsRequest.serialize,
                response_deserializer=service.ListConferenceRecordsResponse.deserialize,
            )
        return self._stubs["list_conference_records"]

    @property
    def get_participant(
        self,
    ) -> Callable[[service.GetParticipantRequest], resource.Participant]:
        r"""Return a callable for the get participant method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a participant by participant ID.

        Returns:
            Callable[[~.GetParticipantRequest],
                    ~.Participant]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_participant" not in self._stubs:
            self._stubs["get_participant"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/GetParticipant",
                request_serializer=service.GetParticipantRequest.serialize,
                response_deserializer=resource.Participant.deserialize,
            )
        return self._stubs["get_participant"]

    @property
    def list_participants(
        self,
    ) -> Callable[[service.ListParticipantsRequest], service.ListParticipantsResponse]:
        r"""Return a callable for the list participants method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the participants in a conference record, by default
        ordered by join time and in descending order. This API supports
        ``fields`` as standard parameters like every other API. However,
        when the ``fields`` request parameter is omitted, this API
        defaults to ``'participants/*, next_page_token'``.

        Returns:
            Callable[[~.ListParticipantsRequest],
                    ~.ListParticipantsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_participants" not in self._stubs:
            self._stubs["list_participants"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/ListParticipants",
                request_serializer=service.ListParticipantsRequest.serialize,
                response_deserializer=service.ListParticipantsResponse.deserialize,
            )
        return self._stubs["list_participants"]

    @property
    def get_participant_session(
        self,
    ) -> Callable[[service.GetParticipantSessionRequest], resource.ParticipantSession]:
        r"""Return a callable for the get participant session method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a participant session by participant session ID.

        Returns:
            Callable[[~.GetParticipantSessionRequest],
                    ~.ParticipantSession]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_participant_session" not in self._stubs:
            self._stubs["get_participant_session"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/GetParticipantSession",
                request_serializer=service.GetParticipantSessionRequest.serialize,
                response_deserializer=resource.ParticipantSession.deserialize,
            )
        return self._stubs["get_participant_session"]

    @property
    def list_participant_sessions(
        self,
    ) -> Callable[
        [service.ListParticipantSessionsRequest],
        service.ListParticipantSessionsResponse,
    ]:
        r"""Return a callable for the list participant sessions method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the participant sessions of a participant in a conference
        record, by default ordered by join time and in descending order.
        This API supports ``fields`` as standard parameters like every
        other API. However, when the ``fields`` request parameter is
        omitted this API defaults to
        ``'participantsessions/*, next_page_token'``.

        Returns:
            Callable[[~.ListParticipantSessionsRequest],
                    ~.ListParticipantSessionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_participant_sessions" not in self._stubs:
            self._stubs["list_participant_sessions"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/ListParticipantSessions",
                request_serializer=service.ListParticipantSessionsRequest.serialize,
                response_deserializer=service.ListParticipantSessionsResponse.deserialize,
            )
        return self._stubs["list_participant_sessions"]

    @property
    def get_recording(
        self,
    ) -> Callable[[service.GetRecordingRequest], resource.Recording]:
        r"""Return a callable for the get recording method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a recording by recording ID.

        Returns:
            Callable[[~.GetRecordingRequest],
                    ~.Recording]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_recording" not in self._stubs:
            self._stubs["get_recording"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/GetRecording",
                request_serializer=service.GetRecordingRequest.serialize,
                response_deserializer=resource.Recording.deserialize,
            )
        return self._stubs["get_recording"]

    @property
    def list_recordings(
        self,
    ) -> Callable[[service.ListRecordingsRequest], service.ListRecordingsResponse]:
        r"""Return a callable for the list recordings method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the recording resources from the conference record.

        Returns:
            Callable[[~.ListRecordingsRequest],
                    ~.ListRecordingsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_recordings" not in self._stubs:
            self._stubs["list_recordings"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/ListRecordings",
                request_serializer=service.ListRecordingsRequest.serialize,
                response_deserializer=service.ListRecordingsResponse.deserialize,
            )
        return self._stubs["list_recordings"]

    @property
    def get_transcript(
        self,
    ) -> Callable[[service.GetTranscriptRequest], resource.Transcript]:
        r"""Return a callable for the get transcript method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a transcript by transcript ID.

        Returns:
            Callable[[~.GetTranscriptRequest],
                    ~.Transcript]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_transcript" not in self._stubs:
            self._stubs["get_transcript"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/GetTranscript",
                request_serializer=service.GetTranscriptRequest.serialize,
                response_deserializer=resource.Transcript.deserialize,
            )
        return self._stubs["get_transcript"]

    @property
    def list_transcripts(
        self,
    ) -> Callable[[service.ListTranscriptsRequest], service.ListTranscriptsResponse]:
        r"""Return a callable for the list transcripts method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the set of transcripts from the conference record.

        Returns:
            Callable[[~.ListTranscriptsRequest],
                    ~.ListTranscriptsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_transcripts" not in self._stubs:
            self._stubs["list_transcripts"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/ListTranscripts",
                request_serializer=service.ListTranscriptsRequest.serialize,
                response_deserializer=service.ListTranscriptsResponse.deserialize,
            )
        return self._stubs["list_transcripts"]

    @property
    def get_transcript_entry(
        self,
    ) -> Callable[[service.GetTranscriptEntryRequest], resource.TranscriptEntry]:
        r"""Return a callable for the get transcript entry method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Gets a ``TranscriptEntry`` resource by entry ID.

        Note: The transcript entries returned by the Google Meet API
        might not match the transcription found in the Google Docs
        transcript file. This can occur when the Google Docs transcript
        file is modified after generation.

        Returns:
            Callable[[~.GetTranscriptEntryRequest],
                    ~.TranscriptEntry]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_transcript_entry" not in self._stubs:
            self._stubs["get_transcript_entry"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/GetTranscriptEntry",
                request_serializer=service.GetTranscriptEntryRequest.serialize,
                response_deserializer=resource.TranscriptEntry.deserialize,
            )
        return self._stubs["get_transcript_entry"]

    @property
    def list_transcript_entries(
        self,
    ) -> Callable[
        [service.ListTranscriptEntriesRequest], service.ListTranscriptEntriesResponse
    ]:
        r"""Return a callable for the list transcript entries method over gRPC.

        `Developer
        Preview <https://developers.google.com/workspace/preview>`__.
        Lists the structured transcript entries per transcript. By
        default, ordered by start time and in ascending order.

        Note: The transcript entries returned by the Google Meet API
        might not match the transcription found in the Google Docs
        transcript file. This can occur when the Google Docs transcript
        file is modified after generation.

        Returns:
            Callable[[~.ListTranscriptEntriesRequest],
                    ~.ListTranscriptEntriesResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_transcript_entries" not in self._stubs:
            self._stubs["list_transcript_entries"] = self._logged_channel.unary_unary(
                "/google.apps.meet.v2beta.ConferenceRecordsService/ListTranscriptEntries",
                request_serializer=service.ListTranscriptEntriesRequest.serialize,
                response_deserializer=service.ListTranscriptEntriesResponse.deserialize,
            )
        return self._stubs["list_transcript_entries"]

    def close(self):
        self._logged_channel.close()

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = ("ConferenceRecordsServiceGrpcTransport",)
