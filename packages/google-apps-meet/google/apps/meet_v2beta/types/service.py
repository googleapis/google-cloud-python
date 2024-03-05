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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import field_mask_pb2  # type: ignore
import proto  # type: ignore

from google.apps.meet_v2beta.types import resource

__protobuf__ = proto.module(
    package="google.apps.meet.v2beta",
    manifest={
        "CreateSpaceRequest",
        "GetSpaceRequest",
        "UpdateSpaceRequest",
        "EndActiveConferenceRequest",
        "GetConferenceRecordRequest",
        "ListConferenceRecordsRequest",
        "ListConferenceRecordsResponse",
        "GetParticipantRequest",
        "ListParticipantsRequest",
        "ListParticipantsResponse",
        "GetParticipantSessionRequest",
        "ListParticipantSessionsRequest",
        "ListParticipantSessionsResponse",
        "GetRecordingRequest",
        "ListRecordingsRequest",
        "ListRecordingsResponse",
        "GetTranscriptRequest",
        "ListTranscriptsRequest",
        "ListTranscriptsResponse",
        "GetTranscriptEntryRequest",
        "ListTranscriptEntriesRequest",
        "ListTranscriptEntriesResponse",
    },
)


class CreateSpaceRequest(proto.Message):
    r"""Request to create a space.

    Attributes:
        space (google.apps.meet_v2beta.types.Space):
            Space to be created. As of May 2023, the
            input space can be empty. Later on the input
            space can be non-empty when space configuration
            is introduced.
    """

    space: resource.Space = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resource.Space,
    )


class GetSpaceRequest(proto.Message):
    r"""Request to get a space.

    Attributes:
        name (str):
            Required. Resource name of the space.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateSpaceRequest(proto.Message):
    r"""Request to update a space.

    Attributes:
        space (google.apps.meet_v2beta.types.Space):
            Required. Space to be updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. Field mask used to specify the fields to be
            updated in the space. If update_mask isn't provided, it
            defaults to '*' and updates all fields provided in the
            request, including deleting fields not set in the request.
    """

    space: resource.Space = proto.Field(
        proto.MESSAGE,
        number=1,
        message=resource.Space,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class EndActiveConferenceRequest(proto.Message):
    r"""Request to end an ongoing conference of a space.

    Attributes:
        name (str):
            Required. Resource name of the space.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetConferenceRecordRequest(proto.Message):
    r"""Request to get a conference record.

    Attributes:
        name (str):
            Required. Resource name of the conference.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListConferenceRecordsRequest(proto.Message):
    r"""Request to fetch list of conference records per user.

    Attributes:
        page_size (int):
            Optional. Maximum number of conference
            records to return. The service might return
            fewer than this value. If unspecified, at most
            25 conference records are returned. The maximum
            value is 100; values above 100 are coerced to
            100. Maximum might change in the future.
        page_token (str):
            Optional. Page token returned from previous
            List Call.
        filter (str):
            Optional. User specified filtering condition in EBNF format.
            The following are the filterable fields:

            -  ``space.meeting_code``
            -  ``space.name``
            -  ``start_time``
            -  ``end_time``

            For example, ``space.meeting_code = "abc-mnop-xyz"``.
    """

    page_size: int = proto.Field(
        proto.INT32,
        number=1,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListConferenceRecordsResponse(proto.Message):
    r"""Response of ListConferenceRecords method.

    Attributes:
        conference_records (MutableSequence[google.apps.meet_v2beta.types.ConferenceRecord]):
            List of conferences in one page.
        next_page_token (str):
            Token to be circulated back for further List
            call if current List does NOT include all the
            Conferences. Unset if all conferences have been
            returned.
    """

    @property
    def raw_page(self):
        return self

    conference_records: MutableSequence[
        resource.ConferenceRecord
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resource.ConferenceRecord,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetParticipantRequest(proto.Message):
    r"""Request to get a Participant.

    Attributes:
        name (str):
            Required. Resource name of the participant.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListParticipantsRequest(proto.Message):
    r"""Request to fetch list of participant per conference.

    Attributes:
        parent (str):
            Required. Format: ``conferenceRecords/{conference_record}``
        page_size (int):
            Maximum number of participants to return. The
            service might return fewer than this value.
            If unspecified, at most 100 participants are
            returned. The maximum value is 250; values above
            250 are coerced to 250. Maximum might change in
            the future.
        page_token (str):
            Page token returned from previous List Call.
        filter (str):
            Optional. User specified filtering condition in EBNF format.
            The following are the filterable fields:

            -  ``earliest_start_time``
            -  ``latest_end_time``

            For example, ``latest_end_time IS NULL`` returns active
            participants in the conference.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListParticipantsResponse(proto.Message):
    r"""Response of ListParticipants method.

    Attributes:
        participants (MutableSequence[google.apps.meet_v2beta.types.Participant]):
            List of participants in one page.
        next_page_token (str):
            Token to be circulated back for further List
            call if current List doesn't include all the
            participants. Unset if all participants are
            returned.
        total_size (int):
            Total, exact number of ``participants``. By default, this
            field isn't included in the response. Set the field mask in
            `SystemParameterContext <https://cloud.google.com/apis/docs/system-parameters>`__
            to receive this field in the response.
    """

    @property
    def raw_page(self):
        return self

    participants: MutableSequence[resource.Participant] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resource.Participant,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


class GetParticipantSessionRequest(proto.Message):
    r"""Request to get a participant session.

    Attributes:
        name (str):
            Required. Resource name of the participant.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListParticipantSessionsRequest(proto.Message):
    r"""Request to fetch list of participant sessions per conference
    record per participant.

    Attributes:
        parent (str):
            Required. Format:
            ``conferenceRecords/{conference_record}/participants/{participant}``
        page_size (int):
            Optional. Maximum number of participant
            sessions to return. The service might return
            fewer than this value. If unspecified, at most
            100 participants are returned. The maximum value
            is 250; values above 250 are coerced to 250.
            Maximum might change in the future.
        page_token (str):
            Optional. Page token returned from previous
            List Call.
        filter (str):
            Optional. User specified filtering condition in EBNF format.
            The following are the filterable fields:

            -  ``start_time``
            -  ``end_time``

            For example, ``end_time IS NULL`` returns active participant
            sessions in the conference record.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListParticipantSessionsResponse(proto.Message):
    r"""Response of ListParticipants method.

    Attributes:
        participant_sessions (MutableSequence[google.apps.meet_v2beta.types.ParticipantSession]):
            List of participants in one page.
        next_page_token (str):
            Token to be circulated back for further List
            call if current List doesn't include all the
            participants. Unset if all participants are
            returned.
    """

    @property
    def raw_page(self):
        return self

    participant_sessions: MutableSequence[
        resource.ParticipantSession
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resource.ParticipantSession,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetRecordingRequest(proto.Message):
    r"""Request message for GetRecording method.

    Attributes:
        name (str):
            Required. Resource name of the recording.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListRecordingsRequest(proto.Message):
    r"""Request for ListRecordings method.

    Attributes:
        parent (str):
            Required. Format: ``conferenceRecords/{conference_record}``
        page_size (int):
            Maximum number of recordings to return. The
            service might return fewer than this value.
            If unspecified, at most 10 recordings are
            returned. The maximum value is 100; values above
            100 are coerced to 100. Maximum might change in
            the future.
        page_token (str):
            Page token returned from previous List Call.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListRecordingsResponse(proto.Message):
    r"""Response for ListRecordings method.

    Attributes:
        recordings (MutableSequence[google.apps.meet_v2beta.types.Recording]):
            List of recordings in one page.
        next_page_token (str):
            Token to be circulated back for further List
            call if current List doesn't include all the
            recordings. Unset if all recordings are
            returned.
    """

    @property
    def raw_page(self):
        return self

    recordings: MutableSequence[resource.Recording] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resource.Recording,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetTranscriptRequest(proto.Message):
    r"""Request for GetTranscript method.

    Attributes:
        name (str):
            Required. Resource name of the transcript.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListTranscriptsRequest(proto.Message):
    r"""Request for ListTranscripts method.

    Attributes:
        parent (str):
            Required. Format: ``conferenceRecords/{conference_record}``
        page_size (int):
            Maximum number of transcripts to return. The
            service might return fewer than this value.
            If unspecified, at most 10 transcripts are
            returned. The maximum value is 100; values above
            100 are coerced to 100. Maximum might change in
            the future.
        page_token (str):
            Page token returned from previous List Call.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListTranscriptsResponse(proto.Message):
    r"""Response for ListTranscripts method.

    Attributes:
        transcripts (MutableSequence[google.apps.meet_v2beta.types.Transcript]):
            List of transcripts in one page.
        next_page_token (str):
            Token to be circulated back for further List
            call if current List doesn't include all the
            transcripts. Unset if all transcripts are
            returned.
    """

    @property
    def raw_page(self):
        return self

    transcripts: MutableSequence[resource.Transcript] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resource.Transcript,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetTranscriptEntryRequest(proto.Message):
    r"""Request for GetTranscriptEntry method.

    Attributes:
        name (str):
            Required. Resource name of the ``TranscriptEntry``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListTranscriptEntriesRequest(proto.Message):
    r"""Request for ListTranscriptEntries method.

    Attributes:
        parent (str):
            Required. Format:
            ``conferenceRecords/{conference_record}/transcripts/{transcript}``
        page_size (int):
            Maximum number of entries to return. The
            service might return fewer than this value.
            If unspecified, at most 10 entries are returned.
            The maximum value is 100; values above 100 are
            coerced to 100. Maximum might change in the
            future.
        page_token (str):
            Page token returned from previous List Call.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListTranscriptEntriesResponse(proto.Message):
    r"""Response for ListTranscriptEntries method

    Attributes:
        transcript_entries (MutableSequence[google.apps.meet_v2beta.types.TranscriptEntry]):
            List of TranscriptEntries in one page.
        next_page_token (str):
            Token to be circulated back for further List
            call if current List doesn't include all the
            transcript entries. Unset if all entries are
            returned.
    """

    @property
    def raw_page(self):
        return self

    transcript_entries: MutableSequence[resource.TranscriptEntry] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resource.TranscriptEntry,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
