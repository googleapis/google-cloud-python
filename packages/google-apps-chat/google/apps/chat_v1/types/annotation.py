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

import proto  # type: ignore

from google.apps.chat_v1.types import user as gc_user

__protobuf__ = proto.module(
    package="google.chat.v1",
    manifest={
        "AnnotationType",
        "Annotation",
        "UserMentionMetadata",
        "SlashCommandMetadata",
    },
)


class AnnotationType(proto.Enum):
    r"""Type of the annotation.

    Values:
        ANNOTATION_TYPE_UNSPECIFIED (0):
            Default value for the enum. Don't use.
        USER_MENTION (1):
            A user is mentioned.
        SLASH_COMMAND (2):
            A slash command is invoked.
    """
    ANNOTATION_TYPE_UNSPECIFIED = 0
    USER_MENTION = 1
    SLASH_COMMAND = 2


class Annotation(proto.Message):
    r"""Output only. Annotations associated with the plain-text body of the
    message. To add basic formatting to a text message, see `Format text
    messages <https://developers.google.com/chat/format-messages>`__.

    Example plain-text message body:

    ::

       Hello @FooBot how are you!"

    The corresponding annotations metadata:

    ::

       "annotations":[{
         "type":"USER_MENTION",
         "startIndex":6,
         "length":7,
         "userMention": {
           "user": {
             "name":"users/{user}",
             "displayName":"FooBot",
             "avatarUrl":"https://goo.gl/aeDtrS",
             "type":"BOT"
           },
           "type":"MENTION"
          }
       }]

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        type_ (google.apps.chat_v1.types.AnnotationType):
            The type of this annotation.
        start_index (int):
            Start index (0-based, inclusive) in the
            plain-text message body this annotation
            corresponds to.

            This field is a member of `oneof`_ ``_start_index``.
        length (int):
            Length of the substring in the plain-text
            message body this annotation corresponds to.
        user_mention (google.apps.chat_v1.types.UserMentionMetadata):
            The metadata of user mention.

            This field is a member of `oneof`_ ``metadata``.
        slash_command (google.apps.chat_v1.types.SlashCommandMetadata):
            The metadata for a slash command.

            This field is a member of `oneof`_ ``metadata``.
    """

    type_: "AnnotationType" = proto.Field(
        proto.ENUM,
        number=1,
        enum="AnnotationType",
    )
    start_index: int = proto.Field(
        proto.INT32,
        number=2,
        optional=True,
    )
    length: int = proto.Field(
        proto.INT32,
        number=3,
    )
    user_mention: "UserMentionMetadata" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="metadata",
        message="UserMentionMetadata",
    )
    slash_command: "SlashCommandMetadata" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="metadata",
        message="SlashCommandMetadata",
    )


class UserMentionMetadata(proto.Message):
    r"""Annotation metadata for user mentions (@).

    Attributes:
        user (google.apps.chat_v1.types.User):
            The user mentioned.
        type_ (google.apps.chat_v1.types.UserMentionMetadata.Type):
            The type of user mention.
    """

    class Type(proto.Enum):
        r"""

        Values:
            TYPE_UNSPECIFIED (0):
                Default value for the enum. Don't use.
            ADD (1):
                Add user to space.
            MENTION (2):
                Mention user in space.
        """
        TYPE_UNSPECIFIED = 0
        ADD = 1
        MENTION = 2

    user: gc_user.User = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gc_user.User,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=2,
        enum=Type,
    )


class SlashCommandMetadata(proto.Message):
    r"""Annotation metadata for slash commands (/).

    Attributes:
        bot (google.apps.chat_v1.types.User):
            The Chat app whose command was invoked.
        type_ (google.apps.chat_v1.types.SlashCommandMetadata.Type):
            The type of slash command.
        command_name (str):
            The name of the invoked slash command.
        command_id (int):
            The command ID of the invoked slash command.
        triggers_dialog (bool):
            Indicates whether the slash command is for a
            dialog.
    """

    class Type(proto.Enum):
        r"""

        Values:
            TYPE_UNSPECIFIED (0):
                Default value for the enum. Don't use.
            ADD (1):
                Add Chat app to space.
            INVOKE (2):
                Invoke slash command in space.
        """
        TYPE_UNSPECIFIED = 0
        ADD = 1
        INVOKE = 2

    bot: gc_user.User = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gc_user.User,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=2,
        enum=Type,
    )
    command_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    command_id: int = proto.Field(
        proto.INT64,
        number=4,
    )
    triggers_dialog: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
