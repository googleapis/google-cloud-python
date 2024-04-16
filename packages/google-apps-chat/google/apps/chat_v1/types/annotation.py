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

from google.apps.chat_v1.types import attachment
from google.apps.chat_v1.types import user as gc_user

__protobuf__ = proto.module(
    package="google.chat.v1",
    manifest={
        "AnnotationType",
        "Annotation",
        "UserMentionMetadata",
        "SlashCommandMetadata",
        "RichLinkMetadata",
        "DriveLinkData",
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
        RICH_LINK (3):
            A rich link annotation.
    """
    ANNOTATION_TYPE_UNSPECIFIED = 0
    USER_MENTION = 1
    SLASH_COMMAND = 2
    RICH_LINK = 3


class Annotation(proto.Message):
    r"""Output only. Annotations associated with the plain-text body of the
    message. To add basic formatting to a text message, see `Format text
    messages <https://developers.google.com/workspace/chat/format-messages>`__.

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
        rich_link_metadata (google.apps.chat_v1.types.RichLinkMetadata):
            The metadata for a rich link.

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
    rich_link_metadata: "RichLinkMetadata" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="metadata",
        message="RichLinkMetadata",
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


class RichLinkMetadata(proto.Message):
    r"""A rich link to a resource.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        uri (str):
            The URI of this link.
        rich_link_type (google.apps.chat_v1.types.RichLinkMetadata.RichLinkType):
            The rich link type.
        drive_link_data (google.apps.chat_v1.types.DriveLinkData):
            Data for a drive link.

            This field is a member of `oneof`_ ``data``.
    """

    class RichLinkType(proto.Enum):
        r"""The rich link type. More types might be added in the future.

        Values:
            RICH_LINK_TYPE_UNSPECIFIED (0):
                Default value for the enum. Don't use.
            DRIVE_FILE (1):
                A Google Drive rich link type.
        """
        RICH_LINK_TYPE_UNSPECIFIED = 0
        DRIVE_FILE = 1

    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )
    rich_link_type: RichLinkType = proto.Field(
        proto.ENUM,
        number=2,
        enum=RichLinkType,
    )
    drive_link_data: "DriveLinkData" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="data",
        message="DriveLinkData",
    )


class DriveLinkData(proto.Message):
    r"""Data for Google Drive links.

    Attributes:
        drive_data_ref (google.apps.chat_v1.types.DriveDataRef):
            A
            `DriveDataRef <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages.attachments#drivedataref>`__
            which references a Google Drive file.
        mime_type (str):
            The mime type of the linked Google Drive
            resource.
    """

    drive_data_ref: attachment.DriveDataRef = proto.Field(
        proto.MESSAGE,
        number=1,
        message=attachment.DriveDataRef,
    )
    mime_type: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
