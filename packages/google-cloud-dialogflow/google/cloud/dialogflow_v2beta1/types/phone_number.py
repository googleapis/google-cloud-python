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

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2beta1",
    manifest={
        "PhoneNumber",
        "DeletePhoneNumberRequest",
        "UndeletePhoneNumberRequest",
        "ListPhoneNumbersRequest",
        "ListPhoneNumbersResponse",
        "UpdatePhoneNumberRequest",
    },
)


class PhoneNumber(proto.Message):
    r"""Represents a phone number. ``PhoneNumber`` resources enable phone
    calls to be answered by Dialogflow services and are added to a
    project through a
    [PhoneNumberOrder][google.cloud.dialogflow.v2beta1.PhoneNumberOrder].

    Attributes:
        name (str):
            Optional. The unique identifier of this phone number.
            Required for
            [PhoneNumbers.UpdatePhoneNumber][google.cloud.dialogflow.v2beta1.PhoneNumbers.UpdatePhoneNumber]
            method. Format:
            ``projects/<Project ID>/phoneNumbers/<PhoneNumber ID>``.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/phoneNumbers/<PhoneNumber ID>``.
        phone_number (str):
            Output only. Phone number in
            `E.164 <https://en.wikipedia.org/wiki/E.164>`__ format. An
            example of a correctly formatted phone number: +15556767888.
        conversation_profile (str):
            Optional. The conversation profile calls to this
            ``PhoneNumber`` should use. The project ID here should be
            the same as the one in
            [name][google.cloud.dialogflow.v2beta1.PhoneNumber.name].
            Format:
            ``projects/<Project ID>/conversationProfiles/<ConversationProfile ID>``.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversationProfiles/<ConversationProfile ID>``.
        lifecycle_state (google.cloud.dialogflow_v2beta1.types.PhoneNumber.LifecycleState):
            Output only. The state of the ``PhoneNumber``. Defaults to
            ``ACTIVE``. ``PhoneNumber`` objects set to
            ``DELETE_REQUESTED`` always decline incoming calls and can
            be removed completely within 30 days.
    """

    class LifecycleState(proto.Enum):
        r"""The states that a ``PhoneNumber`` can be in.

        Values:
            LIFECYCLE_STATE_UNSPECIFIED (0):
                This value is never used.
            ACTIVE (1):
                Number is active and can receive phone calls.
            DELETE_REQUESTED (2):
                Number is pending deletion, and cannot
                receive calls.
        """
        LIFECYCLE_STATE_UNSPECIFIED = 0
        ACTIVE = 1
        DELETE_REQUESTED = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    phone_number: str = proto.Field(
        proto.STRING,
        number=2,
    )
    conversation_profile: str = proto.Field(
        proto.STRING,
        number=3,
    )
    lifecycle_state: LifecycleState = proto.Field(
        proto.ENUM,
        number=4,
        enum=LifecycleState,
    )


class DeletePhoneNumberRequest(proto.Message):
    r"""The request message for
    [PhoneNumbers.DeletePhoneNumber][google.cloud.dialogflow.v2beta1.PhoneNumbers.DeletePhoneNumber].

    Attributes:
        name (str):
            Required. The unique identifier of the ``PhoneNumber`` to
            delete. Format:
            ``projects/<Project ID>/phoneNumbers/<PhoneNumber ID>``.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/phoneNumbers/<PhoneNumber ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UndeletePhoneNumberRequest(proto.Message):
    r"""The request message for
    [PhoneNumbers.UndeletePhoneNumber][google.cloud.dialogflow.v2beta1.PhoneNumbers.UndeletePhoneNumber].

    Attributes:
        name (str):
            Required. The unique identifier of the ``PhoneNumber`` to
            delete. Format:
            ``projects/<Project ID>/phoneNumbers/<PhoneNumber ID>``.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/phoneNumbers/<PhoneNumber ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListPhoneNumbersRequest(proto.Message):
    r"""The request message for
    [PhoneNumbers.ListPhoneNumbers][google.cloud.dialogflow.v2beta1.PhoneNumbers.ListPhoneNumbers].

    Attributes:
        parent (str):
            Required. The project to list all ``PhoneNumber`` resources
            from. Format: ``projects/<Project ID>``. Format:
            ``projects/<Project ID>/locations/<Location ID>``.
        page_size (int):
            Optional. The maximum number of items to
            return in a single page. The default value is
            100. The maximum value is 1000.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            list request.
        show_deleted (bool):
            Optional. Controls whether ``PhoneNumber`` resources in the
            [DELETE_REQUESTED][google.cloud.dialogflow.v2beta1.PhoneNumber.LifecycleState.DELETE_REQUESTED]
            state should be returned. Defaults to false.
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
    show_deleted: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class ListPhoneNumbersResponse(proto.Message):
    r"""The response message for
    [PhoneNumbers.ListPhoneNumbers][google.cloud.dialogflow.v2beta1.PhoneNumbers.ListPhoneNumbers].

    Attributes:
        phone_numbers (MutableSequence[google.cloud.dialogflow_v2beta1.types.PhoneNumber]):
            The list of ``PhoneNumber`` resources. There is a maximum
            number of items returned based on the page_size field in the
            request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    phone_numbers: MutableSequence["PhoneNumber"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="PhoneNumber",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class UpdatePhoneNumberRequest(proto.Message):
    r"""The request message for
    [PhoneNumbers.UpdatePhoneNumber][google.cloud.dialogflow.v2beta1.PhoneNumbers.UpdatePhoneNumber].

    Attributes:
        phone_number (google.cloud.dialogflow_v2beta1.types.PhoneNumber):
            Required. The ``PhoneNumber`` to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. The mask to control which fields
            get updated.
    """

    phone_number: "PhoneNumber" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PhoneNumber",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
