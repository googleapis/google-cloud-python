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

import dataclasses
import json  # type: ignore
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1, rest_helpers, rest_streaming
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.requests import AuthorizedSession  # type: ignore
from google.protobuf import json_format
from requests import __version__ as requests_version

from google.apps.meet_v2beta.types import resource, service

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .rest_base import _BaseConferenceRecordsServiceRestTransport

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=f"requests@{requests_version}",
)


class ConferenceRecordsServiceRestInterceptor:
    """Interceptor for ConferenceRecordsService.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the ConferenceRecordsServiceRestTransport.

    .. code-block:: python
        class MyCustomConferenceRecordsServiceInterceptor(ConferenceRecordsServiceRestInterceptor):
            def pre_get_conference_record(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_conference_record(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_participant(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_participant(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_participant_session(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_participant_session(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_recording(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_recording(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_transcript(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_transcript(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_transcript_entry(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_transcript_entry(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_conference_records(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_conference_records(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_participants(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_participants(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_participant_sessions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_participant_sessions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_recordings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_recordings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_transcript_entries(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_transcript_entries(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_transcripts(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_transcripts(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = ConferenceRecordsServiceRestTransport(interceptor=MyCustomConferenceRecordsServiceInterceptor())
        client = ConferenceRecordsServiceClient(transport=transport)


    """

    def pre_get_conference_record(
        self,
        request: service.GetConferenceRecordRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetConferenceRecordRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_conference_record

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_get_conference_record(
        self, response: resource.ConferenceRecord
    ) -> resource.ConferenceRecord:
        """Post-rpc interceptor for get_conference_record

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_participant(
        self,
        request: service.GetParticipantRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetParticipantRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_participant

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_get_participant(
        self, response: resource.Participant
    ) -> resource.Participant:
        """Post-rpc interceptor for get_participant

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_participant_session(
        self,
        request: service.GetParticipantSessionRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetParticipantSessionRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_participant_session

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_get_participant_session(
        self, response: resource.ParticipantSession
    ) -> resource.ParticipantSession:
        """Post-rpc interceptor for get_participant_session

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_recording(
        self, request: service.GetRecordingRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetRecordingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_recording

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_get_recording(self, response: resource.Recording) -> resource.Recording:
        """Post-rpc interceptor for get_recording

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_transcript(
        self, request: service.GetTranscriptRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[service.GetTranscriptRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_transcript

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_get_transcript(self, response: resource.Transcript) -> resource.Transcript:
        """Post-rpc interceptor for get_transcript

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_get_transcript_entry(
        self,
        request: service.GetTranscriptEntryRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.GetTranscriptEntryRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_transcript_entry

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_get_transcript_entry(
        self, response: resource.TranscriptEntry
    ) -> resource.TranscriptEntry:
        """Post-rpc interceptor for get_transcript_entry

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_conference_records(
        self,
        request: service.ListConferenceRecordsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListConferenceRecordsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_conference_records

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_list_conference_records(
        self, response: service.ListConferenceRecordsResponse
    ) -> service.ListConferenceRecordsResponse:
        """Post-rpc interceptor for list_conference_records

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_participants(
        self,
        request: service.ListParticipantsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListParticipantsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_participants

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_list_participants(
        self, response: service.ListParticipantsResponse
    ) -> service.ListParticipantsResponse:
        """Post-rpc interceptor for list_participants

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_participant_sessions(
        self,
        request: service.ListParticipantSessionsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListParticipantSessionsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_participant_sessions

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_list_participant_sessions(
        self, response: service.ListParticipantSessionsResponse
    ) -> service.ListParticipantSessionsResponse:
        """Post-rpc interceptor for list_participant_sessions

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_recordings(
        self,
        request: service.ListRecordingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListRecordingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_recordings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_list_recordings(
        self, response: service.ListRecordingsResponse
    ) -> service.ListRecordingsResponse:
        """Post-rpc interceptor for list_recordings

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_transcript_entries(
        self,
        request: service.ListTranscriptEntriesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListTranscriptEntriesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_transcript_entries

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_list_transcript_entries(
        self, response: service.ListTranscriptEntriesResponse
    ) -> service.ListTranscriptEntriesResponse:
        """Post-rpc interceptor for list_transcript_entries

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response

    def pre_list_transcripts(
        self,
        request: service.ListTranscriptsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[service.ListTranscriptsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_transcripts

        Override in a subclass to manipulate the request or metadata
        before they are sent to the ConferenceRecordsService server.
        """
        return request, metadata

    def post_list_transcripts(
        self, response: service.ListTranscriptsResponse
    ) -> service.ListTranscriptsResponse:
        """Post-rpc interceptor for list_transcripts

        Override in a subclass to manipulate the response
        after it is returned by the ConferenceRecordsService server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class ConferenceRecordsServiceRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: ConferenceRecordsServiceRestInterceptor


class ConferenceRecordsServiceRestTransport(_BaseConferenceRecordsServiceRestTransport):
    """REST backend synchronous transport for ConferenceRecordsService.

    REST API for services dealing with conference records.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1
    """

    def __init__(
        self,
        *,
        host: str = "meet.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[ConferenceRecordsServiceRestInterceptor] = None,
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

            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                certificate to configure mutual TLS HTTP channel. It is ignored
                if ``channel`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you are developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.
            url_scheme: the protocol scheme for the API endpoint.  Normally
                "https", but for testing or local servers,
                "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            url_scheme=url_scheme,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or ConferenceRecordsServiceRestInterceptor()
        self._prep_wrapped_messages(client_info)

    class _GetConferenceRecord(
        _BaseConferenceRecordsServiceRestTransport._BaseGetConferenceRecord,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.GetConferenceRecord")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetConferenceRecordRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resource.ConferenceRecord:
            r"""Call the get conference record method over HTTP.

            Args:
                request (~.service.GetConferenceRecordRequest):
                    The request object. Request to get a conference record.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resource.ConferenceRecord:
                    `Developer
                Preview <https://developers.google.com/workspace/preview>`__.
                Single instance of a meeting held in a space.

            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseGetConferenceRecord._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_conference_record(
                request, metadata
            )
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseGetConferenceRecord._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseGetConferenceRecord._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConferenceRecordsServiceRestTransport._GetConferenceRecord._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resource.ConferenceRecord()
            pb_resp = resource.ConferenceRecord.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_conference_record(resp)
            return resp

    class _GetParticipant(
        _BaseConferenceRecordsServiceRestTransport._BaseGetParticipant,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.GetParticipant")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetParticipantRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resource.Participant:
            r"""Call the get participant method over HTTP.

            Args:
                request (~.service.GetParticipantRequest):
                    The request object. Request to get a Participant.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resource.Participant:
                    `Developer
                Preview <https://developers.google.com/workspace/preview>`__.
                User who attended or is attending a conference.

            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseGetParticipant._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_participant(request, metadata)
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseGetParticipant._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseGetParticipant._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ConferenceRecordsServiceRestTransport._GetParticipant._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resource.Participant()
            pb_resp = resource.Participant.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_participant(resp)
            return resp

    class _GetParticipantSession(
        _BaseConferenceRecordsServiceRestTransport._BaseGetParticipantSession,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.GetParticipantSession")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetParticipantSessionRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resource.ParticipantSession:
            r"""Call the get participant session method over HTTP.

            Args:
                request (~.service.GetParticipantSessionRequest):
                    The request object. Request to get a participant session.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resource.ParticipantSession:
                    `Developer
                Preview <https://developers.google.com/workspace/preview>`__.
                Refers to each unique join/leave session when a user
                joins a conference from a device. Note that any time a
                user joins the conference a new unique ID is assigned.
                That means if a user joins a space multiple times from
                the same device, they're assigned different IDs, and are
                also be treated as different participant sessions.

            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseGetParticipantSession._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_participant_session(
                request, metadata
            )
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseGetParticipantSession._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseGetParticipantSession._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConferenceRecordsServiceRestTransport._GetParticipantSession._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resource.ParticipantSession()
            pb_resp = resource.ParticipantSession.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_participant_session(resp)
            return resp

    class _GetRecording(
        _BaseConferenceRecordsServiceRestTransport._BaseGetRecording,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.GetRecording")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetRecordingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resource.Recording:
            r"""Call the get recording method over HTTP.

            Args:
                request (~.service.GetRecordingRequest):
                    The request object. Request message for GetRecording
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resource.Recording:
                    `Developer
                Preview <https://developers.google.com/workspace/preview>`__.
                Metadata about a recording created during a conference.

            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseGetRecording._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_recording(request, metadata)
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseGetRecording._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseGetRecording._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ConferenceRecordsServiceRestTransport._GetRecording._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resource.Recording()
            pb_resp = resource.Recording.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_recording(resp)
            return resp

    class _GetTranscript(
        _BaseConferenceRecordsServiceRestTransport._BaseGetTranscript,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.GetTranscript")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetTranscriptRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resource.Transcript:
            r"""Call the get transcript method over HTTP.

            Args:
                request (~.service.GetTranscriptRequest):
                    The request object. Request for GetTranscript method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resource.Transcript:
                    `Developer
                Preview <https://developers.google.com/workspace/preview>`__.
                Metadata for a transcript generated from a conference.
                It refers to the ASR (Automatic Speech Recognition)
                result of user's speech during the conference.

            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseGetTranscript._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_transcript(request, metadata)
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseGetTranscript._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseGetTranscript._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ConferenceRecordsServiceRestTransport._GetTranscript._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resource.Transcript()
            pb_resp = resource.Transcript.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_transcript(resp)
            return resp

    class _GetTranscriptEntry(
        _BaseConferenceRecordsServiceRestTransport._BaseGetTranscriptEntry,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.GetTranscriptEntry")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.GetTranscriptEntryRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resource.TranscriptEntry:
            r"""Call the get transcript entry method over HTTP.

            Args:
                request (~.service.GetTranscriptEntryRequest):
                    The request object. Request for GetTranscriptEntry
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resource.TranscriptEntry:
                    `Developer
                Preview <https://developers.google.com/workspace/preview>`__.
                Single entry for one user’s speech during a transcript
                session.

            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseGetTranscriptEntry._get_http_options()
            )
            request, metadata = self._interceptor.pre_get_transcript_entry(
                request, metadata
            )
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseGetTranscriptEntry._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseGetTranscriptEntry._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ConferenceRecordsServiceRestTransport._GetTranscriptEntry._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = resource.TranscriptEntry()
            pb_resp = resource.TranscriptEntry.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_transcript_entry(resp)
            return resp

    class _ListConferenceRecords(
        _BaseConferenceRecordsServiceRestTransport._BaseListConferenceRecords,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.ListConferenceRecords")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListConferenceRecordsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListConferenceRecordsResponse:
            r"""Call the list conference records method over HTTP.

            Args:
                request (~.service.ListConferenceRecordsRequest):
                    The request object. Request to fetch list of conference
                records per user.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListConferenceRecordsResponse:
                    Response of ListConferenceRecords
                method.

            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseListConferenceRecords._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_conference_records(
                request, metadata
            )
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseListConferenceRecords._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseListConferenceRecords._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConferenceRecordsServiceRestTransport._ListConferenceRecords._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListConferenceRecordsResponse()
            pb_resp = service.ListConferenceRecordsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_conference_records(resp)
            return resp

    class _ListParticipants(
        _BaseConferenceRecordsServiceRestTransport._BaseListParticipants,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.ListParticipants")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListParticipantsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListParticipantsResponse:
            r"""Call the list participants method over HTTP.

            Args:
                request (~.service.ListParticipantsRequest):
                    The request object. Request to fetch list of participant
                per conference.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListParticipantsResponse:
                    Response of ListParticipants method.
            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseListParticipants._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_participants(
                request, metadata
            )
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseListParticipants._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseListParticipants._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ConferenceRecordsServiceRestTransport._ListParticipants._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListParticipantsResponse()
            pb_resp = service.ListParticipantsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_participants(resp)
            return resp

    class _ListParticipantSessions(
        _BaseConferenceRecordsServiceRestTransport._BaseListParticipantSessions,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.ListParticipantSessions")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListParticipantSessionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListParticipantSessionsResponse:
            r"""Call the list participant sessions method over HTTP.

            Args:
                request (~.service.ListParticipantSessionsRequest):
                    The request object. Request to fetch list of participant
                sessions per conference record per
                participant.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListParticipantSessionsResponse:
                    Response of ListParticipants method.
            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseListParticipantSessions._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_participant_sessions(
                request, metadata
            )
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseListParticipantSessions._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseListParticipantSessions._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConferenceRecordsServiceRestTransport._ListParticipantSessions._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListParticipantSessionsResponse()
            pb_resp = service.ListParticipantSessionsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_participant_sessions(resp)
            return resp

    class _ListRecordings(
        _BaseConferenceRecordsServiceRestTransport._BaseListRecordings,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.ListRecordings")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListRecordingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListRecordingsResponse:
            r"""Call the list recordings method over HTTP.

            Args:
                request (~.service.ListRecordingsRequest):
                    The request object. Request for ListRecordings method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListRecordingsResponse:
                    Response for ListRecordings method.
            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseListRecordings._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_recordings(request, metadata)
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseListRecordings._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseListRecordings._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ConferenceRecordsServiceRestTransport._ListRecordings._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListRecordingsResponse()
            pb_resp = service.ListRecordingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_recordings(resp)
            return resp

    class _ListTranscriptEntries(
        _BaseConferenceRecordsServiceRestTransport._BaseListTranscriptEntries,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.ListTranscriptEntries")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListTranscriptEntriesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListTranscriptEntriesResponse:
            r"""Call the list transcript entries method over HTTP.

            Args:
                request (~.service.ListTranscriptEntriesRequest):
                    The request object. Request for ListTranscriptEntries
                method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListTranscriptEntriesResponse:
                    Response for ListTranscriptEntries
                method

            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseListTranscriptEntries._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_transcript_entries(
                request, metadata
            )
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseListTranscriptEntries._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseListTranscriptEntries._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = ConferenceRecordsServiceRestTransport._ListTranscriptEntries._get_response(
                self._host,
                metadata,
                query_params,
                self._session,
                timeout,
                transcoded_request,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListTranscriptEntriesResponse()
            pb_resp = service.ListTranscriptEntriesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_transcript_entries(resp)
            return resp

    class _ListTranscripts(
        _BaseConferenceRecordsServiceRestTransport._BaseListTranscripts,
        ConferenceRecordsServiceRestStub,
    ):
        def __hash__(self):
            return hash("ConferenceRecordsServiceRestTransport.ListTranscripts")

        @staticmethod
        def _get_response(
            host,
            metadata,
            query_params,
            session,
            timeout,
            transcoded_request,
            body=None,
        ):
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(session, method)(
                "{host}{uri}".format(host=host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )
            return response

        def __call__(
            self,
            request: service.ListTranscriptsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> service.ListTranscriptsResponse:
            r"""Call the list transcripts method over HTTP.

            Args:
                request (~.service.ListTranscriptsRequest):
                    The request object. Request for ListTranscripts method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.service.ListTranscriptsResponse:
                    Response for ListTranscripts method.
            """

            http_options = (
                _BaseConferenceRecordsServiceRestTransport._BaseListTranscripts._get_http_options()
            )
            request, metadata = self._interceptor.pre_list_transcripts(
                request, metadata
            )
            transcoded_request = _BaseConferenceRecordsServiceRestTransport._BaseListTranscripts._get_transcoded_request(
                http_options, request
            )

            # Jsonify the query params
            query_params = _BaseConferenceRecordsServiceRestTransport._BaseListTranscripts._get_query_params_json(
                transcoded_request
            )

            # Send the request
            response = (
                ConferenceRecordsServiceRestTransport._ListTranscripts._get_response(
                    self._host,
                    metadata,
                    query_params,
                    self._session,
                    timeout,
                    transcoded_request,
                )
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = service.ListTranscriptsResponse()
            pb_resp = service.ListTranscriptsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_transcripts(resp)
            return resp

    @property
    def get_conference_record(
        self,
    ) -> Callable[[service.GetConferenceRecordRequest], resource.ConferenceRecord]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetConferenceRecord(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_participant(
        self,
    ) -> Callable[[service.GetParticipantRequest], resource.Participant]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetParticipant(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_participant_session(
        self,
    ) -> Callable[[service.GetParticipantSessionRequest], resource.ParticipantSession]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetParticipantSession(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_recording(
        self,
    ) -> Callable[[service.GetRecordingRequest], resource.Recording]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRecording(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_transcript(
        self,
    ) -> Callable[[service.GetTranscriptRequest], resource.Transcript]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTranscript(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_transcript_entry(
        self,
    ) -> Callable[[service.GetTranscriptEntryRequest], resource.TranscriptEntry]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetTranscriptEntry(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_conference_records(
        self,
    ) -> Callable[
        [service.ListConferenceRecordsRequest], service.ListConferenceRecordsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListConferenceRecords(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_participants(
        self,
    ) -> Callable[[service.ListParticipantsRequest], service.ListParticipantsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListParticipants(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_participant_sessions(
        self,
    ) -> Callable[
        [service.ListParticipantSessionsRequest],
        service.ListParticipantSessionsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListParticipantSessions(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_recordings(
        self,
    ) -> Callable[[service.ListRecordingsRequest], service.ListRecordingsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRecordings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_transcript_entries(
        self,
    ) -> Callable[
        [service.ListTranscriptEntriesRequest], service.ListTranscriptEntriesResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTranscriptEntries(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_transcripts(
        self,
    ) -> Callable[[service.ListTranscriptsRequest], service.ListTranscriptsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListTranscripts(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("ConferenceRecordsServiceRestTransport",)
