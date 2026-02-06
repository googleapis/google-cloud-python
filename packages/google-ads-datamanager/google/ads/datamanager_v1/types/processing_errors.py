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
        "ProcessingErrorReason",
        "ProcessingWarningReason",
        "ErrorInfo",
        "ErrorCount",
        "WarningInfo",
        "WarningCount",
    },
)


class ProcessingErrorReason(proto.Enum):
    r"""The processing error reason.

    Values:
        PROCESSING_ERROR_REASON_UNSPECIFIED (0):
            The processing error reason is unknown.
        PROCESSING_ERROR_REASON_INVALID_CUSTOM_VARIABLE (1):
            The custom variable is invalid.
        PROCESSING_ERROR_REASON_CUSTOM_VARIABLE_NOT_ENABLED (2):
            The status of the custom variable is not
            enabled.
        PROCESSING_ERROR_REASON_EVENT_TOO_OLD (3):
            The conversion is older than max supported
            age.
        PROCESSING_ERROR_REASON_DENIED_CONSENT (4):
            The ad user data is denied, either by the
            user or in the advertiser default settings.
        PROCESSING_ERROR_REASON_NO_CONSENT (5):
            Advertiser did not give 3P consent for the
            Ads core platform services.
        PROCESSING_ERROR_REASON_UNKNOWN_CONSENT (6):
            The overall consent (determined from row
            level consent, request level consent, and
            account settings) could not be determined for
            this user
        PROCESSING_ERROR_REASON_DUPLICATE_GCLID (7):
            A conversion with the same GCLID and
            conversion time already exists in the system.
        PROCESSING_ERROR_REASON_DUPLICATE_TRANSACTION_ID (8):
            A conversion with the same order id and
            conversion action combination was already
            uploaded.
        PROCESSING_ERROR_REASON_INVALID_GBRAID (9):
            The gbraid could not be decoded.
        PROCESSING_ERROR_REASON_INVALID_GCLID (10):
            The google click ID could not be decoded.
        PROCESSING_ERROR_REASON_INVALID_MERCHANT_ID (11):
            Merchant id contains non-digit characters.
        PROCESSING_ERROR_REASON_INVALID_WBRAID (12):
            The wbraid could not be decoded.
        PROCESSING_ERROR_REASON_INTERNAL_ERROR (13):
            Internal error.
        PROCESSING_ERROR_REASON_DESTINATION_ACCOUNT_ENHANCED_CONVERSIONS_TERMS_NOT_SIGNED (14):
            Enhanced conversions terms are not signed in
            the destination account.
        PROCESSING_ERROR_REASON_INVALID_EVENT (15):
            The event is invalid.
        PROCESSING_ERROR_REASON_INSUFFICIENT_MATCHED_TRANSACTIONS (16):
            The matched transactions are less than the
            minimum threshold.
        PROCESSING_ERROR_REASON_INSUFFICIENT_TRANSACTIONS (17):
            The transactions are less than the minimum
            threshold.
        PROCESSING_ERROR_REASON_INVALID_FORMAT (18):
            The event has format error.
        PROCESSING_ERROR_REASON_DECRYPTION_ERROR (19):
            The event has a decryption error.
        PROCESSING_ERROR_REASON_DEK_DECRYPTION_ERROR (20):
            The DEK failed to be decrypted.
        PROCESSING_ERROR_REASON_INVALID_WIP (21):
            The WIP is formatted incorrectly or the WIP
            does not exist.
        PROCESSING_ERROR_REASON_INVALID_KEK (22):
            The KEK cannot decrypt data because it is the
            wrong KEK, or it does not exist.
        PROCESSING_ERROR_REASON_WIP_AUTH_FAILED (23):
            The WIP could not be used because it was
            rejected by its attestation condition.
        PROCESSING_ERROR_REASON_KEK_PERMISSION_DENIED (24):
            The system did not have the permissions
            needed to access the KEK.
        PROCESSING_ERROR_REASON_AWS_AUTH_FAILED (27):
            The system failed to authenticate with AWS.
        PROCESSING_ERROR_REASON_USER_IDENTIFIER_DECRYPTION_ERROR (25):
            Failed to decrypt the
            [UserIdentifier][google.ads.datamanager.v1.UserIdentifier]
            data using the DEK.
        PROCESSING_ERROR_OPERATING_ACCOUNT_MISMATCH_FOR_AD_IDENTIFIER (26):
            The user attempted to ingest events with an
            ad identifier that isn't from the operating
            account's ads.
    """

    PROCESSING_ERROR_REASON_UNSPECIFIED = 0
    PROCESSING_ERROR_REASON_INVALID_CUSTOM_VARIABLE = 1
    PROCESSING_ERROR_REASON_CUSTOM_VARIABLE_NOT_ENABLED = 2
    PROCESSING_ERROR_REASON_EVENT_TOO_OLD = 3
    PROCESSING_ERROR_REASON_DENIED_CONSENT = 4
    PROCESSING_ERROR_REASON_NO_CONSENT = 5
    PROCESSING_ERROR_REASON_UNKNOWN_CONSENT = 6
    PROCESSING_ERROR_REASON_DUPLICATE_GCLID = 7
    PROCESSING_ERROR_REASON_DUPLICATE_TRANSACTION_ID = 8
    PROCESSING_ERROR_REASON_INVALID_GBRAID = 9
    PROCESSING_ERROR_REASON_INVALID_GCLID = 10
    PROCESSING_ERROR_REASON_INVALID_MERCHANT_ID = 11
    PROCESSING_ERROR_REASON_INVALID_WBRAID = 12
    PROCESSING_ERROR_REASON_INTERNAL_ERROR = 13
    PROCESSING_ERROR_REASON_DESTINATION_ACCOUNT_ENHANCED_CONVERSIONS_TERMS_NOT_SIGNED = 14
    PROCESSING_ERROR_REASON_INVALID_EVENT = 15
    PROCESSING_ERROR_REASON_INSUFFICIENT_MATCHED_TRANSACTIONS = 16
    PROCESSING_ERROR_REASON_INSUFFICIENT_TRANSACTIONS = 17
    PROCESSING_ERROR_REASON_INVALID_FORMAT = 18
    PROCESSING_ERROR_REASON_DECRYPTION_ERROR = 19
    PROCESSING_ERROR_REASON_DEK_DECRYPTION_ERROR = 20
    PROCESSING_ERROR_REASON_INVALID_WIP = 21
    PROCESSING_ERROR_REASON_INVALID_KEK = 22
    PROCESSING_ERROR_REASON_WIP_AUTH_FAILED = 23
    PROCESSING_ERROR_REASON_KEK_PERMISSION_DENIED = 24
    PROCESSING_ERROR_REASON_AWS_AUTH_FAILED = 27
    PROCESSING_ERROR_REASON_USER_IDENTIFIER_DECRYPTION_ERROR = 25
    PROCESSING_ERROR_OPERATING_ACCOUNT_MISMATCH_FOR_AD_IDENTIFIER = 26


class ProcessingWarningReason(proto.Enum):
    r"""The processing warning reason.

    Values:
        PROCESSING_WARNING_REASON_UNSPECIFIED (0):
            The processing warning reason is unknown.
        PROCESSING_WARNING_REASON_KEK_PERMISSION_DENIED (1):
            The system did not have the permissions
            needed to access the KEK.
        PROCESSING_WARNING_REASON_DEK_DECRYPTION_ERROR (2):
            The DEK failed to be decrypted.
        PROCESSING_WARNING_REASON_DECRYPTION_ERROR (3):
            The event has a decryption error.
        PROCESSING_WARNING_REASON_WIP_AUTH_FAILED (4):
            The WIP could not be used because it was
            rejected by its attestation condition.
        PROCESSING_WARNING_REASON_INVALID_WIP (5):
            The WIP is formatted incorrectly or the WIP
            does not exist.
        PROCESSING_WARNING_REASON_INVALID_KEK (6):
            The KEK cannot decrypt data because it is the
            wrong KEK, or it does not exist.
        PROCESSING_WARNING_REASON_USER_IDENTIFIER_DECRYPTION_ERROR (7):
            Failed to decrypt th
            [UserIdentifier][google.ads.datamanager.v1.UserIdentifier]
            data using the DEK.
        PROCESSING_WARNING_REASON_INTERNAL_ERROR (8):
            Internal error.
        PROCESSING_WARNING_REASON_AWS_AUTH_FAILED (9):
            The system failed to authenticate with AWS.
    """

    PROCESSING_WARNING_REASON_UNSPECIFIED = 0
    PROCESSING_WARNING_REASON_KEK_PERMISSION_DENIED = 1
    PROCESSING_WARNING_REASON_DEK_DECRYPTION_ERROR = 2
    PROCESSING_WARNING_REASON_DECRYPTION_ERROR = 3
    PROCESSING_WARNING_REASON_WIP_AUTH_FAILED = 4
    PROCESSING_WARNING_REASON_INVALID_WIP = 5
    PROCESSING_WARNING_REASON_INVALID_KEK = 6
    PROCESSING_WARNING_REASON_USER_IDENTIFIER_DECRYPTION_ERROR = 7
    PROCESSING_WARNING_REASON_INTERNAL_ERROR = 8
    PROCESSING_WARNING_REASON_AWS_AUTH_FAILED = 9


class ErrorInfo(proto.Message):
    r"""Error counts for each type of error.

    Attributes:
        error_counts (MutableSequence[google.ads.datamanager_v1.types.ErrorCount]):
            A list of errors and counts per error reason.
            May not be populated in all cases.
    """

    error_counts: MutableSequence["ErrorCount"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ErrorCount",
    )


class ErrorCount(proto.Message):
    r"""The error count for a given error reason.

    Attributes:
        record_count (int):
            The count of records that failed to upload
            for a given reason.
        reason (google.ads.datamanager_v1.types.ProcessingErrorReason):
            The error reason of the failed records.
    """

    record_count: int = proto.Field(
        proto.INT64,
        number=1,
    )
    reason: "ProcessingErrorReason" = proto.Field(
        proto.ENUM,
        number=2,
        enum="ProcessingErrorReason",
    )


class WarningInfo(proto.Message):
    r"""Warning counts for each type of warning.

    Attributes:
        warning_counts (MutableSequence[google.ads.datamanager_v1.types.WarningCount]):
            A list of warnings and counts per warning
            reason.
    """

    warning_counts: MutableSequence["WarningCount"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="WarningCount",
    )


class WarningCount(proto.Message):
    r"""The warning count for a given warning reason.

    Attributes:
        record_count (int):
            The count of records that have a warning.
        reason (google.ads.datamanager_v1.types.ProcessingWarningReason):
            The warning reason.
    """

    record_count: int = proto.Field(
        proto.INT64,
        number=1,
    )
    reason: "ProcessingWarningReason" = proto.Field(
        proto.ENUM,
        number=2,
        enum="ProcessingWarningReason",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
