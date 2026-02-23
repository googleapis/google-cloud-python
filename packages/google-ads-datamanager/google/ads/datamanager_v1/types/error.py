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

__protobuf__ = proto.module(
    package="google.ads.datamanager.v1",
    manifest={
        "ErrorReason",
    },
)


class ErrorReason(proto.Enum):
    r"""Error reasons for Data Manager API.

    Values:
        ERROR_REASON_UNSPECIFIED (0):
            Do not use this default value.
        INTERNAL_ERROR (1):
            An internal error has occurred.
        DEADLINE_EXCEEDED (2):
            The request took too long to respond.
        RESOURCE_EXHAUSTED (3):
            Too many requests.
        NOT_FOUND (4):
            Resource not found.
        PERMISSION_DENIED (5):
            The user does not have permission or the
            resource is not found.
        INVALID_ARGUMENT (6):
            There was a problem with the request.
        REQUIRED_FIELD_MISSING (7):
            Required field is missing.
        INVALID_FORMAT (8):
            Format is invalid.
        INVALID_HEX_ENCODING (9):
            The HEX encoded value is malformed.
        INVALID_BASE64_ENCODING (10):
            The base64 encoded value is malformed.
        INVALID_SHA256_FORMAT (11):
            The SHA256 encoded value is malformed.
        INVALID_POSTAL_CODE (12):
            Postal code is not valid.
        INVALID_COUNTRY_CODE (13):
            Country code is not valid.
        INVALID_ENUM_VALUE (14):
            Enum value cannot be used.
        INVALID_USER_LIST_TYPE (15):
            Type of the user list is not applicable for
            this request.
        INVALID_AUDIENCE_MEMBER (16):
            This audience member is not valid.
        TOO_MANY_AUDIENCE_MEMBERS (17):
            Maximum number of audience members allowed
            per request is 10,000.
        TOO_MANY_USER_IDENTIFIERS (18):
            Maximum number of user identifiers allowed
            per audience member is 10.
        TOO_MANY_DESTINATIONS (19):
            Maximum number of destinations allowed per
            request is 10.
        INVALID_DESTINATION (20):
            This Destination is not valid.
        DATA_PARTNER_USER_LIST_MUTATE_NOT_ALLOWED (21):
            Data Partner does not have access to the
            operating account owned userlist.
        INVALID_MOBILE_ID_FORMAT (22):
            Mobile ID format is not valid.
        INVALID_USER_LIST_ID (23):
            User list is not valid.
        MULTIPLE_DATA_TYPES_NOT_ALLOWED (24):
            Multiple data types are not allowed to be
            ingested in a single request.
        DIFFERENT_LOGIN_ACCOUNTS_NOT_ALLOWED_FOR_DATA_PARTNER (25):
            Destination configs containing a DataPartner
            login account must have the same login account
            across all destination configs.
        TERMS_AND_CONDITIONS_NOT_SIGNED (26):
            Required terms and conditions are not
            accepted.
        INVALID_NUMBER_FORMAT (27):
            Invalid number format.
        INVALID_CONVERSION_ACTION_ID (28):
            Conversion action ID is not valid.
        INVALID_CONVERSION_ACTION_TYPE (29):
            The conversion action type is not valid.
        INVALID_CURRENCY_CODE (30):
            The currency code is not supported.
        INVALID_EVENT (31):
            This event is not valid.
        TOO_MANY_EVENTS (32):
            Maximum number of events allowed per request
            is 10,000.
        DESTINATION_ACCOUNT_NOT_ENABLED_ENHANCED_CONVERSIONS_FOR_LEADS (33):
            The destination account is not enabled for
            enhanced conversions for leads.
        DESTINATION_ACCOUNT_DATA_POLICY_PROHIBITS_ENHANCED_CONVERSIONS (34):
            Enhanced conversions can't be used for the
            destination account because of Google customer
            data policies. Contact your Google
            representative..
        DESTINATION_ACCOUNT_ENHANCED_CONVERSIONS_TERMS_NOT_SIGNED (35):
            The destination account hasn't agreed to the
            terms for enhanced conversions.
        DUPLICATE_DESTINATION_REFERENCE (36):
            Two or more destinations in the request have
            the same reference.
        UNSUPPORTED_OPERATING_ACCOUNT_FOR_DATA_PARTNER (37):
            Unsupported operating account for data
            partner authorization.
        UNSUPPORTED_LINKED_ACCOUNT_FOR_DATA_PARTNER (38):
            Unsupported linked account for data partner
            authorization.
        NO_IDENTIFIERS_PROVIDED (39):
            Events data contains no user identifiers or
            ad identifiers.
        INVALID_PROPERTY_TYPE (40):
            The property type is not supported.
        INVALID_STREAM_TYPE (41):
            The stream type is not supported.
        LINKED_ACCOUNT_ONLY_ALLOWED_WITH_DATA_PARTNER_LOGIN_ACCOUNT (42):
            Linked account is only supported when the login account is a
            ``DATA_PARTNER`` account.
        OPERATING_ACCOUNT_LOGIN_ACCOUNT_MISMATCH (43):
            The login account must be the same as the
            operating account for the given use case.
        EVENT_TIME_INVALID (44):
            Event did not occur within the acceptable
            time window.
        RESERVED_NAME_USED (45):
            Parameter uses a reserved name.
        INVALID_EVENT_NAME (46):
            The event name is not supported.
        NOT_ALLOWLISTED (47):
            The account is not allowlisted for the given
            feature.
        INVALID_REQUEST_ID (48):
            The request ID used to retrieve the status of a request is
            not valid. Status can only be retrieved for requests that
            succeed and don't have ``validate_only=true``.
        MULTIPLE_DESTINATIONS_FOR_GOOGLE_ANALYTICS_EVENT (49):
            An event had 2 or more Google Analytics
            destinations.
        FIELD_VALUE_TOO_LONG (50):
            The field value is too long.
        TOO_MANY_ELEMENTS (51):
            Too many elements in a list in the request.
    """

    ERROR_REASON_UNSPECIFIED = 0
    INTERNAL_ERROR = 1
    DEADLINE_EXCEEDED = 2
    RESOURCE_EXHAUSTED = 3
    NOT_FOUND = 4
    PERMISSION_DENIED = 5
    INVALID_ARGUMENT = 6
    REQUIRED_FIELD_MISSING = 7
    INVALID_FORMAT = 8
    INVALID_HEX_ENCODING = 9
    INVALID_BASE64_ENCODING = 10
    INVALID_SHA256_FORMAT = 11
    INVALID_POSTAL_CODE = 12
    INVALID_COUNTRY_CODE = 13
    INVALID_ENUM_VALUE = 14
    INVALID_USER_LIST_TYPE = 15
    INVALID_AUDIENCE_MEMBER = 16
    TOO_MANY_AUDIENCE_MEMBERS = 17
    TOO_MANY_USER_IDENTIFIERS = 18
    TOO_MANY_DESTINATIONS = 19
    INVALID_DESTINATION = 20
    DATA_PARTNER_USER_LIST_MUTATE_NOT_ALLOWED = 21
    INVALID_MOBILE_ID_FORMAT = 22
    INVALID_USER_LIST_ID = 23
    MULTIPLE_DATA_TYPES_NOT_ALLOWED = 24
    DIFFERENT_LOGIN_ACCOUNTS_NOT_ALLOWED_FOR_DATA_PARTNER = 25
    TERMS_AND_CONDITIONS_NOT_SIGNED = 26
    INVALID_NUMBER_FORMAT = 27
    INVALID_CONVERSION_ACTION_ID = 28
    INVALID_CONVERSION_ACTION_TYPE = 29
    INVALID_CURRENCY_CODE = 30
    INVALID_EVENT = 31
    TOO_MANY_EVENTS = 32
    DESTINATION_ACCOUNT_NOT_ENABLED_ENHANCED_CONVERSIONS_FOR_LEADS = 33
    DESTINATION_ACCOUNT_DATA_POLICY_PROHIBITS_ENHANCED_CONVERSIONS = 34
    DESTINATION_ACCOUNT_ENHANCED_CONVERSIONS_TERMS_NOT_SIGNED = 35
    DUPLICATE_DESTINATION_REFERENCE = 36
    UNSUPPORTED_OPERATING_ACCOUNT_FOR_DATA_PARTNER = 37
    UNSUPPORTED_LINKED_ACCOUNT_FOR_DATA_PARTNER = 38
    NO_IDENTIFIERS_PROVIDED = 39
    INVALID_PROPERTY_TYPE = 40
    INVALID_STREAM_TYPE = 41
    LINKED_ACCOUNT_ONLY_ALLOWED_WITH_DATA_PARTNER_LOGIN_ACCOUNT = 42
    OPERATING_ACCOUNT_LOGIN_ACCOUNT_MISMATCH = 43
    EVENT_TIME_INVALID = 44
    RESERVED_NAME_USED = 45
    INVALID_EVENT_NAME = 46
    NOT_ALLOWLISTED = 47
    INVALID_REQUEST_ID = 48
    MULTIPLE_DESTINATIONS_FOR_GOOGLE_ANALYTICS_EVENT = 49
    FIELD_VALUE_TOO_LONG = 50
    TOO_MANY_ELEMENTS = 51


__all__ = tuple(sorted(__protobuf__.manifest))
