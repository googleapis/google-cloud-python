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

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.chat.v1",
    manifest={
        "DeletionMetadata",
    },
)


class DeletionMetadata(proto.Message):
    r"""Information about a deleted message. A message is deleted when
    ``delete_time`` is set.

    Attributes:
        deletion_type (google.apps.chat_v1.types.DeletionMetadata.DeletionType):
            Indicates who deleted the message.
    """

    class DeletionType(proto.Enum):
        r"""Who deleted the message and how it was deleted. More values
        may be added in the future.

        Values:
            DELETION_TYPE_UNSPECIFIED (0):
                This value is unused.
            CREATOR (1):
                User deleted their own message.
            SPACE_OWNER (2):
                The space owner deleted the message.
            ADMIN (3):
                A Google Workspace admin deleted the message.
            APP_MESSAGE_EXPIRY (4):
                A Chat app deleted its own message when it
                expired.
            CREATOR_VIA_APP (5):
                A Chat app deleted the message on behalf of
                the user.
            SPACE_OWNER_VIA_APP (6):
                A Chat app deleted the message on behalf of
                the space owner.
        """
        DELETION_TYPE_UNSPECIFIED = 0
        CREATOR = 1
        SPACE_OWNER = 2
        ADMIN = 3
        APP_MESSAGE_EXPIRY = 4
        CREATOR_VIA_APP = 5
        SPACE_OWNER_VIA_APP = 6

    deletion_type: DeletionType = proto.Field(
        proto.ENUM,
        number=1,
        enum=DeletionType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
