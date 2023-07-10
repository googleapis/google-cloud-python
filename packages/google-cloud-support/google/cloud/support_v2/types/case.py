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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.support_v2.types import actor

__protobuf__ = proto.module(
    package="google.cloud.support.v2",
    manifest={
        "Case",
        "CaseClassification",
    },
)


class Case(proto.Message):
    r"""A support case.

    Attributes:
        name (str):
            The resource name for the case.
        display_name (str):
            The short summary of the issue reported in
            this case.
        description (str):
            A broad description of the issue.
        classification (google.cloud.support_v2.types.CaseClassification):
            The issue classification applicable to this
            case.
        time_zone (str):
            The timezone of the user who created the
            support case. It should be in a format IANA
            recognizes: https://www.iana.org/time-zones.
            There is no additional validation done by the
            API.
        subscriber_email_addresses (MutableSequence[str]):
            The email addresses to receive updates on
            this case.
        state (google.cloud.support_v2.types.Case.State):
            Output only. The current status of the
            support case.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time this case was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time this case was last
            updated.
        creator (google.cloud.support_v2.types.Actor):
            The user who created the case.
            Note: The name and email will be obfuscated if
            the case was created by Google Support.
        contact_email (str):
            A user-supplied email address to send case
            update notifications for. This should only be
            used in BYOID flows, where we cannot infer the
            user's email address directly from their EUCs.
        escalated (bool):
            Whether the case is currently escalated.
        test_case (bool):
            Whether this case was created for internal
            API testing and should not be acted on by the
            support team.
        language_code (str):
            The language the user has requested to receive support in.
            This should be a BCP 47 language code (e.g., ``"en"``,
            ``"zh-CN"``, ``"zh-TW"``, ``"ja"``, ``"ko"``). If no
            language or an unsupported language is specified, this field
            defaults to English (en).

            Language selection during case creation may affect your
            available support options. For a list of supported languages
            and their support working hours, see:
            https://cloud.google.com/support/docs/language-working-hours
        priority (google.cloud.support_v2.types.Case.Priority):
            The priority of this case.
    """

    class State(proto.Enum):
        r"""The status of a support case.

        Values:
            STATE_UNSPECIFIED (0):
                Case is in an unknown state.
            NEW (1):
                The case has been created but no one is
                assigned to work on it yet.
            IN_PROGRESS_GOOGLE_SUPPORT (2):
                The case is currently being handled by Google
                support.
            ACTION_REQUIRED (3):
                Google is waiting for a response.
            SOLUTION_PROVIDED (4):
                A solution has been offered for the case, but
                it isn't yet closed.
            CLOSED (5):
                The case has been resolved.
        """
        STATE_UNSPECIFIED = 0
        NEW = 1
        IN_PROGRESS_GOOGLE_SUPPORT = 2
        ACTION_REQUIRED = 3
        SOLUTION_PROVIDED = 4
        CLOSED = 5

    class Priority(proto.Enum):
        r"""The case Priority. P0 is most urgent and P4 the least.

        Values:
            PRIORITY_UNSPECIFIED (0):
                Priority is undefined or has not been set
                yet.
            P0 (1):
                Extreme impact on a production service.
                Service is hard down.
            P1 (2):
                Critical impact on a production service.
                Service is currently unusable.
            P2 (3):
                Severe impact on a production service.
                Service is usable but greatly impaired.
            P3 (4):
                Medium impact on a production service.
                Service is available, but moderately impaired.
            P4 (5):
                General questions or minor issues.
                Production service is fully available.
        """
        PRIORITY_UNSPECIFIED = 0
        P0 = 1
        P1 = 2
        P2 = 3
        P3 = 4
        P4 = 5

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    description: str = proto.Field(
        proto.STRING,
        number=3,
    )
    classification: "CaseClassification" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="CaseClassification",
    )
    time_zone: str = proto.Field(
        proto.STRING,
        number=8,
    )
    subscriber_email_addresses: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=9,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=12,
        enum=State,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=13,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=14,
        message=timestamp_pb2.Timestamp,
    )
    creator: actor.Actor = proto.Field(
        proto.MESSAGE,
        number=15,
        message=actor.Actor,
    )
    contact_email: str = proto.Field(
        proto.STRING,
        number=35,
    )
    escalated: bool = proto.Field(
        proto.BOOL,
        number=17,
    )
    test_case: bool = proto.Field(
        proto.BOOL,
        number=19,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=23,
    )
    priority: Priority = proto.Field(
        proto.ENUM,
        number=32,
        enum=Priority,
    )


class CaseClassification(proto.Message):
    r"""A classification object with a product type and value.

    Attributes:
        id (str):
            The unique ID for a classification. Must be specified for
            case creation.

            To retrieve valid classification IDs for case creation, use
            ``caseClassifications.search``.
        display_name (str):
            The display name of the classification.
    """

    id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
