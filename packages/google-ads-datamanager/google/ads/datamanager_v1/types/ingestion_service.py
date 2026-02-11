# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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

import proto  # type: ignore

from google.ads.datamanager_v1.types import audience, destination, event
from google.ads.datamanager_v1.types import consent as gad_consent
from google.ads.datamanager_v1.types import encryption_info as gad_encryption_info
from google.ads.datamanager_v1.types import (
    request_status_per_destination as gad_request_status_per_destination,
)
from google.ads.datamanager_v1.types import terms_of_service as gad_terms_of_service

__protobuf__ = proto.module(
    package="google.ads.datamanager.v1",
    manifest={
        "Encoding",
        "IngestAudienceMembersRequest",
        "IngestAudienceMembersResponse",
        "RemoveAudienceMembersRequest",
        "RemoveAudienceMembersResponse",
        "IngestEventsRequest",
        "IngestEventsResponse",
        "RetrieveRequestStatusRequest",
        "RetrieveRequestStatusResponse",
    },
)


class Encoding(proto.Enum):
    r"""The encoding type of the hashed identifying information.

    Values:
        ENCODING_UNSPECIFIED (0):
            Unspecified Encoding type. Should never be
            used.
        HEX (1):
            Hex encoding.
        BASE64 (2):
            Base 64 encoding.
    """

    ENCODING_UNSPECIFIED = 0
    HEX = 1
    BASE64 = 2


class IngestAudienceMembersRequest(proto.Message):
    r"""Request to upload audience members to the provided destinations.
    Returns an
    [IngestAudienceMembersResponse][google.ads.datamanager.v1.IngestAudienceMembersResponse].

    Attributes:
        destinations (MutableSequence[google.ads.datamanager_v1.types.Destination]):
            Required. The list of destinations to send
            the audience members to.
        audience_members (MutableSequence[google.ads.datamanager_v1.types.AudienceMember]):
            Required. The list of users to send to the specified
            destinations. At most 10000
            [AudienceMember][google.ads.datamanager.v1.AudienceMember]
            resources can be sent in a single request.
        consent (google.ads.datamanager_v1.types.Consent):
            Optional. Request-level consent to apply to all users in the
            request. User-level consent overrides request-level consent,
            and can be specified in each
            [AudienceMember][google.ads.datamanager.v1.AudienceMember].
        validate_only (bool):
            Optional. For testing purposes. If ``true``, the request is
            validated but not executed. Only errors are returned, not
            results.
        encoding (google.ads.datamanager_v1.types.Encoding):
            Optional. Required for
            [UserData][google.ads.datamanager.v1.UserData] uploads. The
            encoding type of the user identifiers. For hashed user
            identifiers, this is the encoding type of the hashed string.
            For encrypted hashed user identifiers, this is the encoding
            type of the outer encrypted string, but not necessarily the
            inner hashed string, meaning the inner hashed string could
            be encoded in a different way than the outer encrypted
            string. For non ``UserData`` uploads, this field is ignored.
        encryption_info (google.ads.datamanager_v1.types.EncryptionInfo):
            Optional. Encryption information for
            [UserData][google.ads.datamanager.v1.UserData] uploads. If
            not set, it's assumed that uploaded identifying information
            is hashed but not encrypted. For non ``UserData`` uploads,
            this field is ignored.
        terms_of_service (google.ads.datamanager_v1.types.TermsOfService):
            Optional. The terms of service that the user
            has accepted/rejected.
    """

    destinations: MutableSequence[destination.Destination] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=destination.Destination,
    )
    audience_members: MutableSequence[audience.AudienceMember] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=audience.AudienceMember,
    )
    consent: gad_consent.Consent = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gad_consent.Consent,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    encoding: "Encoding" = proto.Field(
        proto.ENUM,
        number=5,
        enum="Encoding",
    )
    encryption_info: gad_encryption_info.EncryptionInfo = proto.Field(
        proto.MESSAGE,
        number=6,
        message=gad_encryption_info.EncryptionInfo,
    )
    terms_of_service: gad_terms_of_service.TermsOfService = proto.Field(
        proto.MESSAGE,
        number=7,
        message=gad_terms_of_service.TermsOfService,
    )


class IngestAudienceMembersResponse(proto.Message):
    r"""Response from the
    [IngestAudienceMembersRequest][google.ads.datamanager.v1.IngestAudienceMembersRequest].

    Attributes:
        request_id (str):
            The auto-generated ID of the request.
    """

    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


class RemoveAudienceMembersRequest(proto.Message):
    r"""Request to remove users from an audience in the provided
    destinations. Returns a
    [RemoveAudienceMembersResponse][google.ads.datamanager.v1.RemoveAudienceMembersResponse].

    Attributes:
        destinations (MutableSequence[google.ads.datamanager_v1.types.Destination]):
            Required. The list of destinations to remove
            the users from.
        audience_members (MutableSequence[google.ads.datamanager_v1.types.AudienceMember]):
            Required. The list of users to remove.
        validate_only (bool):
            Optional. For testing purposes. If ``true``, the request is
            validated but not executed. Only errors are returned, not
            results.
        encoding (google.ads.datamanager_v1.types.Encoding):
            Optional. Required for
            [UserData][google.ads.datamanager.v1.UserData] uploads. The
            encoding type of the user identifiers. Applies to only the
            outer encoding for encrypted user identifiers. For non
            ``UserData`` uploads, this field is ignored.
        encryption_info (google.ads.datamanager_v1.types.EncryptionInfo):
            Optional. Encryption information for
            [UserData][google.ads.datamanager.v1.UserData] uploads. If
            not set, it's assumed that uploaded identifying information
            is hashed but not encrypted. For non ``UserData`` uploads,
            this field is ignored.
    """

    destinations: MutableSequence[destination.Destination] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=destination.Destination,
    )
    audience_members: MutableSequence[audience.AudienceMember] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=audience.AudienceMember,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    encoding: "Encoding" = proto.Field(
        proto.ENUM,
        number=4,
        enum="Encoding",
    )
    encryption_info: gad_encryption_info.EncryptionInfo = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gad_encryption_info.EncryptionInfo,
    )


class RemoveAudienceMembersResponse(proto.Message):
    r"""Response from the
    [RemoveAudienceMembersRequest][google.ads.datamanager.v1.RemoveAudienceMembersRequest].

    Attributes:
        request_id (str):
            The auto-generated ID of the request.
    """

    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


class IngestEventsRequest(proto.Message):
    r"""Request to upload audience members to the provided destinations.
    Returns an
    [IngestEventsResponse][google.ads.datamanager.v1.IngestEventsResponse].

    Attributes:
        destinations (MutableSequence[google.ads.datamanager_v1.types.Destination]):
            Required. The list of destinations to send
            the events to.
        events (MutableSequence[google.ads.datamanager_v1.types.Event]):
            Required. The list of events to send to the specified
            destinations. At most 2000
            [Event][google.ads.datamanager.v1.Event] resources can be
            sent in a single request.
        consent (google.ads.datamanager_v1.types.Consent):
            Optional. Request-level consent to apply to all users in the
            request. User-level consent overrides request-level consent,
            and can be specified in each
            [Event][google.ads.datamanager.v1.Event].
        validate_only (bool):
            Optional. For testing purposes. If ``true``, the request is
            validated but not executed. Only errors are returned, not
            results.
        encoding (google.ads.datamanager_v1.types.Encoding):
            Optional. Required for
            [UserData][google.ads.datamanager.v1.UserData] uploads. The
            encoding type of the user identifiers. For hashed user
            identifiers, this is the encoding type of the hashed string.
            For encrypted hashed user identifiers, this is the encoding
            type of the outer encrypted string, but not necessarily the
            inner hashed string, meaning the inner hashed string could
            be encoded in a different way than the outer encrypted
            string. For non ``UserData`` uploads, this field is ignored.
        encryption_info (google.ads.datamanager_v1.types.EncryptionInfo):
            Optional. Encryption information for
            [UserData][google.ads.datamanager.v1.UserData] uploads. If
            not set, it's assumed that uploaded identifying information
            is hashed but not encrypted. For non ``UserData`` uploads,
            this field is ignored.
    """

    destinations: MutableSequence[destination.Destination] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=destination.Destination,
    )
    events: MutableSequence[event.Event] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=event.Event,
    )
    consent: gad_consent.Consent = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gad_consent.Consent,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    encoding: "Encoding" = proto.Field(
        proto.ENUM,
        number=5,
        enum="Encoding",
    )
    encryption_info: gad_encryption_info.EncryptionInfo = proto.Field(
        proto.MESSAGE,
        number=6,
        message=gad_encryption_info.EncryptionInfo,
    )


class IngestEventsResponse(proto.Message):
    r"""Response from the
    [IngestEventsRequest][google.ads.datamanager.v1.IngestEventsRequest].

    Attributes:
        request_id (str):
            The auto-generated ID of the request.
    """

    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


class RetrieveRequestStatusRequest(proto.Message):
    r"""Request to get the status of request made to the DM API for a given
    request ID. Returns a
    [RetrieveRequestStatusResponse][google.ads.datamanager.v1.RetrieveRequestStatusResponse].

    Attributes:
        request_id (str):
            Required. Required. The request ID of the
            Data Manager API request.
    """

    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


class RetrieveRequestStatusResponse(proto.Message):
    r"""Response from the
    [RetrieveRequestStatusRequest][google.ads.datamanager.v1.RetrieveRequestStatusRequest].

    Attributes:
        request_status_per_destination (MutableSequence[google.ads.datamanager_v1.types.RequestStatusPerDestination]):
            A list of request statuses per destination.
            The order of the statuses matches the order of
            the destinations in the original request.
    """

    request_status_per_destination: MutableSequence[
        gad_request_status_per_destination.RequestStatusPerDestination
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gad_request_status_per_destination.RequestStatusPerDestination,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
