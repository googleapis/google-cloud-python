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
from google.apps.meet import gapic_version as package_version

__version__ = package_version.__version__


from google.apps.meet_v2beta.services.conference_records_service.client import ConferenceRecordsServiceClient
from google.apps.meet_v2beta.services.conference_records_service.async_client import ConferenceRecordsServiceAsyncClient
from google.apps.meet_v2beta.services.spaces_service.client import SpacesServiceClient
from google.apps.meet_v2beta.services.spaces_service.async_client import SpacesServiceAsyncClient

from google.apps.meet_v2beta.types.resource import ActiveConference
from google.apps.meet_v2beta.types.resource import AnonymousUser
from google.apps.meet_v2beta.types.resource import ConferenceRecord
from google.apps.meet_v2beta.types.resource import DocsDestination
from google.apps.meet_v2beta.types.resource import DriveDestination
from google.apps.meet_v2beta.types.resource import Participant
from google.apps.meet_v2beta.types.resource import ParticipantSession
from google.apps.meet_v2beta.types.resource import PhoneUser
from google.apps.meet_v2beta.types.resource import Recording
from google.apps.meet_v2beta.types.resource import SignedinUser
from google.apps.meet_v2beta.types.resource import Space
from google.apps.meet_v2beta.types.resource import SpaceConfig
from google.apps.meet_v2beta.types.resource import Transcript
from google.apps.meet_v2beta.types.resource import TranscriptEntry
from google.apps.meet_v2beta.types.service import CreateSpaceRequest
from google.apps.meet_v2beta.types.service import EndActiveConferenceRequest
from google.apps.meet_v2beta.types.service import GetConferenceRecordRequest
from google.apps.meet_v2beta.types.service import GetParticipantRequest
from google.apps.meet_v2beta.types.service import GetParticipantSessionRequest
from google.apps.meet_v2beta.types.service import GetRecordingRequest
from google.apps.meet_v2beta.types.service import GetSpaceRequest
from google.apps.meet_v2beta.types.service import GetTranscriptEntryRequest
from google.apps.meet_v2beta.types.service import GetTranscriptRequest
from google.apps.meet_v2beta.types.service import ListConferenceRecordsRequest
from google.apps.meet_v2beta.types.service import ListConferenceRecordsResponse
from google.apps.meet_v2beta.types.service import ListParticipantSessionsRequest
from google.apps.meet_v2beta.types.service import ListParticipantSessionsResponse
from google.apps.meet_v2beta.types.service import ListParticipantsRequest
from google.apps.meet_v2beta.types.service import ListParticipantsResponse
from google.apps.meet_v2beta.types.service import ListRecordingsRequest
from google.apps.meet_v2beta.types.service import ListRecordingsResponse
from google.apps.meet_v2beta.types.service import ListTranscriptEntriesRequest
from google.apps.meet_v2beta.types.service import ListTranscriptEntriesResponse
from google.apps.meet_v2beta.types.service import ListTranscriptsRequest
from google.apps.meet_v2beta.types.service import ListTranscriptsResponse
from google.apps.meet_v2beta.types.service import UpdateSpaceRequest

__all__ = ('ConferenceRecordsServiceClient',
    'ConferenceRecordsServiceAsyncClient',
    'SpacesServiceClient',
    'SpacesServiceAsyncClient',
    'ActiveConference',
    'AnonymousUser',
    'ConferenceRecord',
    'DocsDestination',
    'DriveDestination',
    'Participant',
    'ParticipantSession',
    'PhoneUser',
    'Recording',
    'SignedinUser',
    'Space',
    'SpaceConfig',
    'Transcript',
    'TranscriptEntry',
    'CreateSpaceRequest',
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
    'UpdateSpaceRequest',
)
