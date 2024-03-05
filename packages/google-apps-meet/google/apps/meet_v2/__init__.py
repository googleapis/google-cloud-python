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
from google.apps.meet_v2 import gapic_version as package_version

__version__ = package_version.__version__


from .services.conference_records_service import (
    ConferenceRecordsServiceAsyncClient,
    ConferenceRecordsServiceClient,
)
from .services.spaces_service import SpacesServiceAsyncClient, SpacesServiceClient
from .types.resource import (
    ActiveConference,
    AnonymousUser,
    ConferenceRecord,
    DocsDestination,
    DriveDestination,
    Participant,
    ParticipantSession,
    PhoneUser,
    Recording,
    SignedinUser,
    Space,
    SpaceConfig,
    Transcript,
    TranscriptEntry,
)
from .types.service import (
    CreateSpaceRequest,
    EndActiveConferenceRequest,
    GetConferenceRecordRequest,
    GetParticipantRequest,
    GetParticipantSessionRequest,
    GetRecordingRequest,
    GetSpaceRequest,
    GetTranscriptEntryRequest,
    GetTranscriptRequest,
    ListConferenceRecordsRequest,
    ListConferenceRecordsResponse,
    ListParticipantSessionsRequest,
    ListParticipantSessionsResponse,
    ListParticipantsRequest,
    ListParticipantsResponse,
    ListRecordingsRequest,
    ListRecordingsResponse,
    ListTranscriptEntriesRequest,
    ListTranscriptEntriesResponse,
    ListTranscriptsRequest,
    ListTranscriptsResponse,
    UpdateSpaceRequest,
)

__all__ = (
    "ConferenceRecordsServiceAsyncClient",
    "SpacesServiceAsyncClient",
    "ActiveConference",
    "AnonymousUser",
    "ConferenceRecord",
    "ConferenceRecordsServiceClient",
    "CreateSpaceRequest",
    "DocsDestination",
    "DriveDestination",
    "EndActiveConferenceRequest",
    "GetConferenceRecordRequest",
    "GetParticipantRequest",
    "GetParticipantSessionRequest",
    "GetRecordingRequest",
    "GetSpaceRequest",
    "GetTranscriptEntryRequest",
    "GetTranscriptRequest",
    "ListConferenceRecordsRequest",
    "ListConferenceRecordsResponse",
    "ListParticipantSessionsRequest",
    "ListParticipantSessionsResponse",
    "ListParticipantsRequest",
    "ListParticipantsResponse",
    "ListRecordingsRequest",
    "ListRecordingsResponse",
    "ListTranscriptEntriesRequest",
    "ListTranscriptEntriesResponse",
    "ListTranscriptsRequest",
    "ListTranscriptsResponse",
    "Participant",
    "ParticipantSession",
    "PhoneUser",
    "Recording",
    "SignedinUser",
    "Space",
    "SpaceConfig",
    "SpacesServiceClient",
    "Transcript",
    "TranscriptEntry",
    "UpdateSpaceRequest",
)
