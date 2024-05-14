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

from google.apps.chat_v1.types import user as gc_user

__protobuf__ = proto.module(
    package="google.chat.v1",
    manifest={
        "Reaction",
        "Emoji",
        "CustomEmoji",
        "EmojiReactionSummary",
        "CreateReactionRequest",
        "ListReactionsRequest",
        "ListReactionsResponse",
        "DeleteReactionRequest",
    },
)


class Reaction(proto.Message):
    r"""A reaction to a message.

    Attributes:
        name (str):
            The resource name of the reaction.

            Format:
            ``spaces/{space}/messages/{message}/reactions/{reaction}``
        user (google.apps.chat_v1.types.User):
            Output only. The user who created the
            reaction.
        emoji (google.apps.chat_v1.types.Emoji):
            The emoji used in the reaction.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    user: gc_user.User = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gc_user.User,
    )
    emoji: "Emoji" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Emoji",
    )


class Emoji(proto.Message):
    r"""An emoji that is used as a reaction to a message.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        unicode (str):
            A basic emoji represented by a unicode
            string.

            This field is a member of `oneof`_ ``content``.
        custom_emoji (google.apps.chat_v1.types.CustomEmoji):
            Output only. A custom emoji.

            This field is a member of `oneof`_ ``content``.
    """

    unicode: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="content",
    )
    custom_emoji: "CustomEmoji" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="content",
        message="CustomEmoji",
    )


class CustomEmoji(proto.Message):
    r"""Represents a custom emoji.

    Attributes:
        uid (str):
            Output only. Unique key for the custom emoji
            resource.
    """

    uid: str = proto.Field(
        proto.STRING,
        number=1,
    )


class EmojiReactionSummary(proto.Message):
    r"""The number of people who reacted to a message with a specific
    emoji.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        emoji (google.apps.chat_v1.types.Emoji):
            Emoji associated with the reactions.
        reaction_count (int):
            The total number of reactions using the
            associated emoji.

            This field is a member of `oneof`_ ``_reaction_count``.
    """

    emoji: "Emoji" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Emoji",
    )
    reaction_count: int = proto.Field(
        proto.INT32,
        number=2,
        optional=True,
    )


class CreateReactionRequest(proto.Message):
    r"""Creates a reaction to a message.

    Attributes:
        parent (str):
            Required. The message where the reaction is created.

            Format: ``spaces/{space}/messages/{message}``
        reaction (google.apps.chat_v1.types.Reaction):
            Required. The reaction to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    reaction: "Reaction" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Reaction",
    )


class ListReactionsRequest(proto.Message):
    r"""Lists reactions to a message.

    Attributes:
        parent (str):
            Required. The message users reacted to.

            Format: ``spaces/{space}/messages/{message}``
        page_size (int):
            Optional. The maximum number of reactions
            returned. The service can return fewer reactions
            than this value. If unspecified, the default
            value is 25. The maximum value is 200; values
            above 200 are changed to 200.
        page_token (str):
            Optional. (If resuming from a previous
            query.)
            A page token received from a previous list
            reactions call. Provide this to retrieve the
            subsequent page.

            When paginating, the filter value should match
            the call that provided the page token. Passing a
            different value might lead to unexpected
            results.
        filter (str):
            Optional. A query filter.

            You can filter reactions by
            `emoji <https://developers.google.com/workspace/chat/api/reference/rest/v1/Emoji>`__
            (either ``emoji.unicode`` or ``emoji.custom_emoji.uid``) and
            `user <https://developers.google.com/workspace/chat/api/reference/rest/v1/User>`__
            (``user.name``).

            To filter reactions for multiple emojis or users, join
            similar fields with the ``OR`` operator, such as
            ``emoji.unicode = "🙂" OR emoji.unicode = "👍"`` and
            ``user.name = "users/AAAAAA" OR user.name = "users/BBBBBB"``.

            To filter reactions by emoji and user, use the ``AND``
            operator, such as
            ``emoji.unicode = "🙂" AND user.name = "users/AAAAAA"``.

            If your query uses both ``AND`` and ``OR``, group them with
            parentheses.

            For example, the following queries are valid:

            ::

               user.name = "users/{user}"
               emoji.unicode = "🙂"
               emoji.custom_emoji.uid = "{uid}"
               emoji.unicode = "🙂" OR emoji.unicode = "👍"
               emoji.unicode = "🙂" OR emoji.custom_emoji.uid = "{uid}"
               emoji.unicode = "🙂" AND user.name = "users/{user}"
               (emoji.unicode = "🙂" OR emoji.custom_emoji.uid = "{uid}")
               AND user.name = "users/{user}"

            The following queries are invalid:

            ::

               emoji.unicode = "🙂" AND emoji.unicode = "👍"
               emoji.unicode = "🙂" AND emoji.custom_emoji.uid = "{uid}"
               emoji.unicode = "🙂" OR user.name = "users/{user}"
               emoji.unicode = "🙂" OR emoji.custom_emoji.uid = "{uid}" OR
               user.name = "users/{user}"
               emoji.unicode = "🙂" OR emoji.custom_emoji.uid = "{uid}"
               AND user.name = "users/{user}"

            Invalid queries are rejected by the server with an
            ``INVALID_ARGUMENT`` error.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListReactionsResponse(proto.Message):
    r"""Response to a list reactions request.

    Attributes:
        reactions (MutableSequence[google.apps.chat_v1.types.Reaction]):
            List of reactions in the requested (or first)
            page.
        next_page_token (str):
            Continuation token to retrieve the next page
            of results. It's empty for the last page of
            results.
    """

    @property
    def raw_page(self):
        return self

    reactions: MutableSequence["Reaction"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Reaction",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DeleteReactionRequest(proto.Message):
    r"""Deletes a reaction to a message.

    Attributes:
        name (str):
            Required. Name of the reaction to delete.

            Format:
            ``spaces/{space}/messages/{message}/reactions/{reaction}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
