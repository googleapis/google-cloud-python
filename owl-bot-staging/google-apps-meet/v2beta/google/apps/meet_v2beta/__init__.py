# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.apps.meet_v2beta import gapic_version as package_version

__version__ = package_version.__version__


from .services.conference_records_service import ConferenceRecordsServiceClient
from .services.conference_records_service import ConferenceRecordsServiceAsyncClient
from .services.spaces_service import SpacesServiceClient
from .services.spaces_service import SpacesServiceAsyncClient

from .types.resource import ActiveConference
from .types.resource import AnonymousUser
from .types.resource import ConferenceRecord
from .types.resource import DocsDestination
from .types.resource import DriveDestination
from .types.resource import Participant
from .types.resource import ParticipantSession
from .types.resource import PhoneUser
from .types.resource import Recording
from .types.resource import SignedinUser
from .types.resource import Space
from .types.resource import SpaceConfig
from .types.resource import Transcript
from .types.resource import TranscriptEntry
from .types.service import CreateSpaceRequest
from .types.service import EndActiveConferenceRequest
from .types.service import GetConferenceRecordRequest
from .types.service import GetParticipantRequest
from .types.service import GetParticipantSessionRequest
from .types.service import GetRecordingRequest
from .types.service import GetSpaceRequest
from .types.service import GetTranscriptEntryRequest
from .types.service import GetTranscriptRequest
from .types.service import ListConferenceRecordsRequest
from .types.service import ListConferenceRecordsResponse
from .types.service import ListParticipantSessionsRequest
from .types.service import ListParticipantSessionsResponse
from .types.service import ListParticipantsRequest
from .types.service import ListParticipantsResponse
from .types.service import ListRecordingsRequest
from .types.service import ListRecordingsResponse
from .types.service import ListTranscriptEntriesRequest
from .types.service import ListTranscriptEntriesResponse
from .types.service import ListTranscriptsRequest
from .types.service import ListTranscriptsResponse
from .types.service import UpdateSpaceRequest

__all__ = (
    'ConferenceRecordsServiceAsyncClient',
    'SpacesServiceAsyncClient',
'ActiveConference',
'AnonymousUser',
'ConferenceRecord',
'ConferenceRecordsServiceClient',
'CreateSpaceRequest',
'DocsDestination',
'DriveDestination',
'EndActiveConferenceRequest',
'GetConferenceRecordRequest',
'GetParticipantRequest',
'GetParticipantSessionRequest',
'GetRecordingRequest',
'GetSpaceRequest',
'GetTranscriptEntryRequest',
'GetTranscriptRequest',
'ListConferenceRecordsRequest',
'ListConferenceRecordsResponse',
'ListParticipantSessionsRequest',
'ListParticipantSessionsResponse',
'ListParticipantsRequest',
'ListParticipantsResponse',
'ListRecordingsRequest',
'ListRecordingsResponse',
'ListTranscriptEntriesRequest',
'ListTranscriptEntriesResponse',
'ListTranscriptsRequest',
'ListTranscriptsResponse',
'Participant',
'ParticipantSession',
'PhoneUser',
'Recording',
'SignedinUser',
'Space',
'SpaceConfig',
'SpacesServiceClient',
'Transcript',
'TranscriptEntry',
'UpdateSpaceRequest',
)
