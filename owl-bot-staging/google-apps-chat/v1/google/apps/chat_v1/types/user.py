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
    package='google.chat.v1',
    manifest={
        'User',
    },
)


class User(proto.Message):
    r"""A user in Google Chat. When returned as an output from a request, if
    your Chat app `authenticates as a
    user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
    the output for a ``User`` resource only populates the user's
    ``name`` and ``type``.

    Attributes:
        name (str):
            Resource name for a Google Chat [user][google.chat.v1.User].

            Format: ``users/{user}``. ``users/app`` can be used as an
            alias for the calling app
            [bot][google.chat.v1.User.Type.BOT] user.

            For [human users][google.chat.v1.User.Type.HUMAN],
            ``{user}`` is the same user identifier as:

            -  the ``id`` for the
               `Person <https://developers.google.com/people/api/rest/v1/people>`__
               in the People API. For example, ``users/123456789`` in
               Chat API represents the same person as the ``123456789``
               Person profile ID in People API.

            -  the ``id`` for a
               `user <https://developers.google.com/admin-sdk/directory/reference/rest/v1/users>`__
               in the Admin SDK Directory API.

            -  the user's email address can be used as an alias for
               ``{user}`` in API requests. For example, if the People
               API Person profile ID for ``user@example.com`` is
               ``123456789``, you can use ``users/user@example.com`` as
               an alias to reference ``users/123456789``. Only the
               canonical resource name (for example ``users/123456789``)
               will be returned from the API.
        display_name (str):
            Output only. The user's display name.
        domain_id (str):
            Unique identifier of the user's Google
            Workspace domain.
        type_ (google.apps.chat_v1.types.User.Type):
            User type.
        is_anonymous (bool):
            Output only. When ``true``, the user is deleted or their
            profile is not visible.
    """
    class Type(proto.Enum):
        r"""

        Values:
            TYPE_UNSPECIFIED (0):
                Default value for the enum. DO NOT USE.
            HUMAN (1):
                Human user.
            BOT (2):
                Chat app user.
        """
        TYPE_UNSPECIFIED = 0
        HUMAN = 1
        BOT = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    domain_id: str = proto.Field(
        proto.STRING,
        number=6,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=5,
        enum=Type,
    )
    is_anonymous: bool = proto.Field(
        proto.BOOL,
        number=7,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
