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

from google.apps.card_v1.types import card as gac_card
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.apps.chat_v1.types import action_status as gc_action_status
from google.apps.chat_v1.types import annotation
from google.apps.chat_v1.types import attachment as gc_attachment
from google.apps.chat_v1.types import contextual_addon
from google.apps.chat_v1.types import deletion_metadata as gc_deletion_metadata
from google.apps.chat_v1.types import matched_url as gc_matched_url
from google.apps.chat_v1.types import reaction
from google.apps.chat_v1.types import slash_command as gc_slash_command
from google.apps.chat_v1.types import space as gc_space
from google.apps.chat_v1.types import user

__protobuf__ = proto.module(
    package="google.chat.v1",
    manifest={
        "Message",
        "AttachedGif",
        "QuotedMessageMetadata",
        "Thread",
        "ActionResponse",
        "AccessoryWidget",
        "GetMessageRequest",
        "DeleteMessageRequest",
        "UpdateMessageRequest",
        "CreateMessageRequest",
        "ListMessagesRequest",
        "ListMessagesResponse",
        "DialogAction",
        "Dialog",
        "CardWithId",
    },
)


class Message(proto.Message):
    r"""A message in a Google Chat space.

    Attributes:
        name (str):
            Resource name of the message.

            Format: ``spaces/{space}/messages/{message}``

            Where ``{space}`` is the ID of the space where the message
            is posted and ``{message}`` is a system-assigned ID for the
            message. For example,
            ``spaces/AAAAAAAAAAA/messages/BBBBBBBBBBB.BBBBBBBBBBB``.

            If you set a custom ID when you create a message, you can
            use this ID to specify the message in a request by replacing
            ``{message}`` with the value from the
            ``clientAssignedMessageId`` field. For example,
            ``spaces/AAAAAAAAAAA/messages/client-custom-name``. For
            details, see `Name a
            message <https://developers.google.com/workspace/chat/create-messages#name_a_created_message>`__.
        sender (google.apps.chat_v1.types.User):
            Output only. The user who created the message. If your Chat
            app `authenticates as a
            user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
            the output populates the
            `user <https://developers.google.com/workspace/chat/api/reference/rest/v1/User>`__
            ``name`` and ``type``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Immutable. For spaces created in
            Chat, the time at which the message was created.
            This field is output only, except when used in
            import mode spaces.

            For import mode spaces, set this field to the
            historical timestamp at which the message was
            created in the source in order to preserve the
            original creation time.
        last_update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the message
            was last edited by a user. If the message has
            never been edited, this field is empty.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time at which the message
            was deleted in Google Chat. If the message is
            never deleted, this field is empty.
        text (str):
            Plain-text body of the message. The first link to an image,
            video, or web page generates a `preview
            chip <https://developers.google.com/workspace/chat/preview-links>`__.
            You can also `@mention a Google Chat
            user <https://developers.google.com/workspace/chat/format-messages#messages-@mention>`__,
            or everyone in the space.

            To learn about creating text messages, see `Send a text
            message <https://developers.google.com/workspace/chat/create-messages#create-text-messages>`__.
        formatted_text (str):
            Output only. Contains the message ``text`` with markups
            added to communicate formatting. This field might not
            capture all formatting visible in the UI, but includes the
            following:

            -  `Markup
               syntax <https://developers.google.com/workspace/chat/format-messages>`__
               for bold, italic, strikethrough, monospace, monospace
               block, and bulleted list.

            -  `User
               mentions <https://developers.google.com/workspace/chat/format-messages#messages-@mention>`__
               using the format ``<users/{user}>``.

            -  Custom hyperlinks using the format
               ``<{url}|{rendered_text}>`` where the first string is the
               URL and the second is the rendered text—for example,
               ``<http://example.com|custom text>``.

            -  Custom emoji using the format ``:{emoji_name}:``—for
               example, ``:smile:``. This doesn't apply to Unicode
               emoji, such as ``U+1F600`` for a grinning face emoji.

            For more information, see `View text formatting sent in a
            message <https://developers.google.com/workspace/chat/format-messages#view_text_formatting_sent_in_a_message>`__
        cards (MutableSequence[google.apps.chat_v1.types.ContextualAddOnMarkup.Card]):
            Deprecated: Use ``cards_v2`` instead.

            Rich, formatted, and interactive cards that you can use to
            display UI elements such as: formatted texts, buttons, and
            clickable images. Cards are normally displayed below the
            plain-text body of the message. ``cards`` and ``cards_v2``
            can have a maximum size of 32 KB.
        cards_v2 (MutableSequence[google.apps.chat_v1.types.CardWithId]):
            An array of
            `cards <https://developers.google.com/workspace/chat/api/reference/rest/v1/cards>`__.

            Only Chat apps can create cards. If your Chat app
            `authenticates as a
            user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
            the messages can't contain cards.

            To learn about cards and how to create them, see `Send card
            messages <https://developers.google.com/workspace/chat/create-messages#create>`__.

            `Card
            builder <https://addons.gsuite.google.com/uikit/builder>`__
        annotations (MutableSequence[google.apps.chat_v1.types.Annotation]):
            Output only. Annotations associated with the ``text`` in
            this message.
        thread (google.apps.chat_v1.types.Thread):
            The thread the message belongs to. For example usage, see
            `Start or reply to a message
            thread <https://developers.google.com/workspace/chat/create-messages#create-message-thread>`__.
        space (google.apps.chat_v1.types.Space):
            If your Chat app `authenticates as a
            user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
            the output populates the
            `space <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces>`__
            ``name``.
        fallback_text (str):
            A plain-text description of the message's
            cards, used when the actual cards can't be
            displayed—for example, mobile notifications.
        action_response (google.apps.chat_v1.types.ActionResponse):
            Input only. Parameters that a Chat app can
            use to configure how its response is posted.
        argument_text (str):
            Output only. Plain-text body of the message
            with all Chat app mentions stripped out.
        slash_command (google.apps.chat_v1.types.SlashCommand):
            Output only. Slash command information, if
            applicable.
        attachment (MutableSequence[google.apps.chat_v1.types.Attachment]):
            User-uploaded attachment.
        matched_url (google.apps.chat_v1.types.MatchedUrl):
            Output only. A URL in ``spaces.messages.text`` that matches
            a link preview pattern. For more information, see `Preview
            links <https://developers.google.com/workspace/chat/preview-links>`__.
        thread_reply (bool):
            Output only. When ``true``, the message is a response in a
            reply thread. When ``false``, the message is visible in the
            space's top-level conversation as either the first message
            of a thread or a message with no threaded replies.

            If the space doesn't support reply in threads, this field is
            always ``false``.
        client_assigned_message_id (str):
            Optional. A custom ID for the message. You can use field to
            identify a message, or to get, delete, or update a message.
            To set a custom ID, specify the
            ```messageId`` <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages/create#body.QUERY_PARAMETERS.message_id>`__
            field when you create the message. For details, see `Name a
            message <https://developers.google.com/workspace/chat/create-messages#name_a_created_message>`__.
        emoji_reaction_summaries (MutableSequence[google.apps.chat_v1.types.EmojiReactionSummary]):
            Output only. The list of emoji reaction
            summaries on the message.
        private_message_viewer (google.apps.chat_v1.types.User):
            Immutable. Input for creating a message, otherwise output
            only. The user that can view the message. When set, the
            message is private and only visible to the specified user
            and the Chat app. Link previews and attachments aren't
            supported for private messages.

            Only Chat apps can send private messages. If your Chat app
            `authenticates as a
            user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__
            to send a message, the message can't be private and must
            omit this field.

            For details, see `Send private messages to Google Chat
            users <https://developers.google.com/workspace/chat/private-messages>`__.
        deletion_metadata (google.apps.chat_v1.types.DeletionMetadata):
            Output only. Information about a deleted message. A message
            is deleted when ``delete_time`` is set.
        quoted_message_metadata (google.apps.chat_v1.types.QuotedMessageMetadata):
            Output only. Information about a message
            that's quoted by a Google Chat user in a space.
            Google Chat users can quote a message to reply
            to it.
        attached_gifs (MutableSequence[google.apps.chat_v1.types.AttachedGif]):
            Output only. GIF images that are attached to
            the message.
        accessory_widgets (MutableSequence[google.apps.chat_v1.types.AccessoryWidget]):
            One or more interactive widgets that appear at the bottom of
            a message. You can add accessory widgets to messages that
            contain text, cards, or both text and cards. Not supported
            for messages that contain dialogs. For details, see `Add
            interactive widgets at the bottom of a
            message <https://developers.google.com/workspace/chat/create-messages#add-accessory-widgets>`__.

            Creating a message with accessory widgets requires [app
            authentication]
            (https://developers.google.com/workspace/chat/authenticate-authorize-chat-app).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    sender: user.User = proto.Field(
        proto.MESSAGE,
        number=2,
        message=user.User,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    last_update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=23,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=26,
        message=timestamp_pb2.Timestamp,
    )
    text: str = proto.Field(
        proto.STRING,
        number=4,
    )
    formatted_text: str = proto.Field(
        proto.STRING,
        number=43,
    )
    cards: MutableSequence[
        contextual_addon.ContextualAddOnMarkup.Card
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=contextual_addon.ContextualAddOnMarkup.Card,
    )
    cards_v2: MutableSequence["CardWithId"] = proto.RepeatedField(
        proto.MESSAGE,
        number=22,
        message="CardWithId",
    )
    annotations: MutableSequence[annotation.Annotation] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=annotation.Annotation,
    )
    thread: "Thread" = proto.Field(
        proto.MESSAGE,
        number=11,
        message="Thread",
    )
    space: gc_space.Space = proto.Field(
        proto.MESSAGE,
        number=12,
        message=gc_space.Space,
    )
    fallback_text: str = proto.Field(
        proto.STRING,
        number=13,
    )
    action_response: "ActionResponse" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="ActionResponse",
    )
    argument_text: str = proto.Field(
        proto.STRING,
        number=15,
    )
    slash_command: gc_slash_command.SlashCommand = proto.Field(
        proto.MESSAGE,
        number=17,
        message=gc_slash_command.SlashCommand,
    )
    attachment: MutableSequence[gc_attachment.Attachment] = proto.RepeatedField(
        proto.MESSAGE,
        number=18,
        message=gc_attachment.Attachment,
    )
    matched_url: gc_matched_url.MatchedUrl = proto.Field(
        proto.MESSAGE,
        number=20,
        message=gc_matched_url.MatchedUrl,
    )
    thread_reply: bool = proto.Field(
        proto.BOOL,
        number=25,
    )
    client_assigned_message_id: str = proto.Field(
        proto.STRING,
        number=32,
    )
    emoji_reaction_summaries: MutableSequence[
        reaction.EmojiReactionSummary
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=33,
        message=reaction.EmojiReactionSummary,
    )
    private_message_viewer: user.User = proto.Field(
        proto.MESSAGE,
        number=36,
        message=user.User,
    )
    deletion_metadata: gc_deletion_metadata.DeletionMetadata = proto.Field(
        proto.MESSAGE,
        number=38,
        message=gc_deletion_metadata.DeletionMetadata,
    )
    quoted_message_metadata: "QuotedMessageMetadata" = proto.Field(
        proto.MESSAGE,
        number=39,
        message="QuotedMessageMetadata",
    )
    attached_gifs: MutableSequence["AttachedGif"] = proto.RepeatedField(
        proto.MESSAGE,
        number=42,
        message="AttachedGif",
    )
    accessory_widgets: MutableSequence["AccessoryWidget"] = proto.RepeatedField(
        proto.MESSAGE,
        number=44,
        message="AccessoryWidget",
    )


class AttachedGif(proto.Message):
    r"""A GIF image that's specified by a URL.

    Attributes:
        uri (str):
            Output only. The URL that hosts the GIF
            image.
    """

    uri: str = proto.Field(
        proto.STRING,
        number=1,
    )


class QuotedMessageMetadata(proto.Message):
    r"""Information about a quoted message.

    Attributes:
        name (str):
            Output only. Resource name of the quoted message.

            Format: ``spaces/{space}/messages/{message}``
        last_update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The timestamp when the quoted
            message was created or when the quoted message
            was last updated.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    last_update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class Thread(proto.Message):
    r"""A thread in a Google Chat space. For example usage, see `Start or
    reply to a message
    thread <https://developers.google.com/workspace/chat/create-messages#create-message-thread>`__.

    If you specify a thread when creating a message, you can set the
    ```messageReplyOption`` <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages/create#messagereplyoption>`__
    field to determine what happens if no matching thread is found.

    Attributes:
        name (str):
            Output only. Resource name of the thread.

            Example: ``spaces/{space}/threads/{thread}``
        thread_key (str):
            Optional. Input for creating or updating a thread.
            Otherwise, output only. ID for the thread. Supports up to
            4000 characters.

            This ID is unique to the Chat app that sets it. For example,
            if multiple Chat apps create a message using the same thread
            key, the messages are posted in different threads. To reply
            in a thread created by a person or another Chat app, specify
            the thread ``name`` field instead.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    thread_key: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ActionResponse(proto.Message):
    r"""Parameters that a Chat app can use to configure how its
    response is posted.

    Attributes:
        type_ (google.apps.chat_v1.types.ActionResponse.ResponseType):
            Input only. The type of Chat app response.
        url (str):
            Input only. URL for users to authenticate or configure.
            (Only for ``REQUEST_CONFIG`` response types.)
        dialog_action (google.apps.chat_v1.types.DialogAction):
            Input only. A response to an interaction event related to a
            `dialog <https://developers.google.com/workspace/chat/dialogs>`__.
            Must be accompanied by ``ResponseType.Dialog``.
        updated_widget (google.apps.chat_v1.types.ActionResponse.UpdatedWidget):
            Input only. The response of the updated
            widget.
    """

    class ResponseType(proto.Enum):
        r"""The type of Chat app response.

        Values:
            TYPE_UNSPECIFIED (0):
                Default type that's handled as ``NEW_MESSAGE``.
            NEW_MESSAGE (1):
                Post as a new message in the topic.
            UPDATE_MESSAGE (2):
                Update the Chat app's message. This is only permitted on a
                ``CARD_CLICKED`` event where the message sender type is
                ``BOT``.
            UPDATE_USER_MESSAGE_CARDS (6):
                Update the cards on a user's message. This is only permitted
                as a response to a ``MESSAGE`` event with a matched url, or
                a ``CARD_CLICKED`` event where the message sender type is
                ``HUMAN``. Text is ignored.
            REQUEST_CONFIG (3):
                Privately ask the user for additional
                authentication or configuration.
            DIALOG (4):
                Presents a
                `dialog <https://developers.google.com/workspace/chat/dialogs>`__.
            UPDATE_WIDGET (7):
                Widget text autocomplete options query.
        """
        TYPE_UNSPECIFIED = 0
        NEW_MESSAGE = 1
        UPDATE_MESSAGE = 2
        UPDATE_USER_MESSAGE_CARDS = 6
        REQUEST_CONFIG = 3
        DIALOG = 4
        UPDATE_WIDGET = 7

    class SelectionItems(proto.Message):
        r"""List of widget autocomplete results.

        Attributes:
            items (MutableSequence[google.apps.card_v1.types.SelectionInput.SelectionItem]):
                An array of the SelectionItem objects.
        """

        items: MutableSequence[
            gac_card.SelectionInput.SelectionItem
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=gac_card.SelectionInput.SelectionItem,
        )

    class UpdatedWidget(proto.Message):
        r"""The response of the updated widget.
        Used to provide autocomplete options for a widget.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            suggestions (google.apps.chat_v1.types.ActionResponse.SelectionItems):
                List of widget autocomplete results

                This field is a member of `oneof`_ ``updated_widget``.
            widget (str):
                The ID of the updated widget. The ID must
                match the one for the widget that triggered the
                update request.
        """

        suggestions: "ActionResponse.SelectionItems" = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="updated_widget",
            message="ActionResponse.SelectionItems",
        )
        widget: str = proto.Field(
            proto.STRING,
            number=2,
        )

    type_: ResponseType = proto.Field(
        proto.ENUM,
        number=1,
        enum=ResponseType,
    )
    url: str = proto.Field(
        proto.STRING,
        number=2,
    )
    dialog_action: "DialogAction" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="DialogAction",
    )
    updated_widget: UpdatedWidget = proto.Field(
        proto.MESSAGE,
        number=4,
        message=UpdatedWidget,
    )


class AccessoryWidget(proto.Message):
    r"""One or more interactive widgets that appear at the bottom of a
    message. For details, see `Add interactive widgets at the bottom of
    a
    message <https://developers.google.com/workspace/chat/create-messages#add-accessory-widgets>`__.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        button_list (google.apps.card_v1.types.ButtonList):
            A list of buttons.

            This field is a member of `oneof`_ ``action``.
    """

    button_list: gac_card.ButtonList = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="action",
        message=gac_card.ButtonList,
    )


class GetMessageRequest(proto.Message):
    r"""Request to get a message.

    Attributes:
        name (str):
            Required. Resource name of the message.

            Format: ``spaces/{space}/messages/{message}``

            If you've set a custom ID for your message, you can use the
            value from the ``clientAssignedMessageId`` field for
            ``{message}``. For details, see [Name a message]
            (https://developers.google.com/workspace/chat/create-messages#name_a_created_message).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteMessageRequest(proto.Message):
    r"""Request to delete a message.

    Attributes:
        name (str):
            Required. Resource name of the message.

            Format: ``spaces/{space}/messages/{message}``

            If you've set a custom ID for your message, you can use the
            value from the ``clientAssignedMessageId`` field for
            ``{message}``. For details, see [Name a message]
            (https://developers.google.com/workspace/chat/create-messages#name_a_created_message).
        force (bool):
            When ``true``, deleting a message also deletes its threaded
            replies. When ``false``, if a message has threaded replies,
            deletion fails.

            Only applies when `authenticating as a
            user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.
            Has no effect when [authenticating as a Chat app]
            (https://developers.google.com/workspace/chat/authenticate-authorize-chat-app).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class UpdateMessageRequest(proto.Message):
    r"""Request to update a message.

    Attributes:
        message (google.apps.chat_v1.types.Message):
            Required. Message with fields updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The field paths to update. Separate multiple
            values with commas or use ``*`` to update all field paths.

            Currently supported field paths:

            -  ``text``

            -  ``attachment``

            -  ``cards`` (Requires `app
               authentication </chat/api/guides/auth/service-accounts>`__.)

            -  ``cards_v2`` (Requires `app
               authentication </chat/api/guides/auth/service-accounts>`__.)

            -  ``accessory_widgets`` (Requires `app
               authentication </chat/api/guides/auth/service-accounts>`__.)
        allow_missing (bool):
            Optional. If ``true`` and the message isn't found, a new
            message is created and ``updateMask`` is ignored. The
            specified message ID must be
            `client-assigned <https://developers.google.com/workspace/chat/create-messages#name_a_created_message>`__
            or the request fails.
    """

    message: "Message" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Message",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    allow_missing: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class CreateMessageRequest(proto.Message):
    r"""Creates a message.

    Attributes:
        parent (str):
            Required. The resource name of the space in which to create
            a message.

            Format: ``spaces/{space}``
        message (google.apps.chat_v1.types.Message):
            Required. Message body.
        thread_key (str):
            Optional. Deprecated: Use
            [thread.thread_key][google.chat.v1.Thread.thread_key]
            instead. ID for the thread. Supports up to 4000 characters.
            To start or add to a thread, create a message and specify a
            ``threadKey`` or the
            [thread.name][google.chat.v1.Thread.name]. For example
            usage, see `Start or reply to a message
            thread <https://developers.google.com/workspace/chat/create-messages#create-message-thread>`__.
        request_id (str):
            Optional. A unique request ID for this
            message. Specifying an existing request ID
            returns the message created with that ID instead
            of creating a new message.
        message_reply_option (google.apps.chat_v1.types.CreateMessageRequest.MessageReplyOption):
            Optional. Specifies whether a message starts
            a thread or replies to one. Only supported in
            named spaces.
        message_id (str):
            Optional. A custom ID for a message. Lets Chat apps get,
            update, or delete a message without needing to store the
            system-assigned ID in the message's resource name
            (represented in the message ``name`` field).

            The value for this field must meet the following
            requirements:

            -  Begins with ``client-``. For example,
               ``client-custom-name`` is a valid custom ID, but
               ``custom-name`` is not.
            -  Contains up to 63 characters and only lowercase letters,
               numbers, and hyphens.
            -  Is unique within a space. A Chat app can't use the same
               custom ID for different messages.

            For details, see `Name a
            message <https://developers.google.com/workspace/chat/create-messages#name_a_created_message>`__.
    """

    class MessageReplyOption(proto.Enum):
        r"""Specifies how to reply to a message.
        More states might be added in the future.

        Values:
            MESSAGE_REPLY_OPTION_UNSPECIFIED (0):
                Default. Starts a new thread. Using this option ignores any
                [thread ID][google.chat.v1.Thread.name] or
                [``thread_key``][google.chat.v1.Thread.thread_key] that's
                included.
            REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD (1):
                Creates the message as a reply to the thread specified by
                [thread ID][google.chat.v1.Thread.name] or
                [``thread_key``][google.chat.v1.Thread.thread_key]. If it
                fails, the message starts a new thread instead.
            REPLY_MESSAGE_OR_FAIL (2):
                Creates the message as a reply to the thread specified by
                [thread ID][google.chat.v1.Thread.name] or
                [``thread_key``][google.chat.v1.Thread.thread_key]. If a new
                ``thread_key`` is used, a new thread is created. If the
                message creation fails, a ``NOT_FOUND`` error is returned
                instead.
        """
        MESSAGE_REPLY_OPTION_UNSPECIFIED = 0
        REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD = 1
        REPLY_MESSAGE_OR_FAIL = 2

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    message: "Message" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="Message",
    )
    thread_key: str = proto.Field(
        proto.STRING,
        number=6,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=7,
    )
    message_reply_option: MessageReplyOption = proto.Field(
        proto.ENUM,
        number=8,
        enum=MessageReplyOption,
    )
    message_id: str = proto.Field(
        proto.STRING,
        number=9,
    )


class ListMessagesRequest(proto.Message):
    r"""Lists messages in the specified space, that the user is a
    member of.

    Attributes:
        parent (str):
            Required. The resource name of the space to list messages
            from.

            Format: ``spaces/{space}``
        page_size (int):
            The maximum number of messages returned. The service might
            return fewer messages than this value.

            If unspecified, at most 25 are returned.

            The maximum value is 1000. If you use a value more than
            1000, it's automatically changed to 1000.

            Negative values return an ``INVALID_ARGUMENT`` error.
        page_token (str):
            Optional, if resuming from a previous query.

            A page token received from a previous list
            messages call. Provide this parameter to
            retrieve the subsequent page.

            When paginating, all other parameters provided
            should match the call that provided the page
            token. Passing different values to the other
            parameters might lead to unexpected results.
        filter (str):
            A query filter.

            You can filter messages by date (``create_time``) and thread
            (``thread.name``).

            To filter messages by the date they were created, specify
            the ``create_time`` with a timestamp in
            `RFC-3339 <https://www.rfc-editor.org/rfc/rfc3339>`__ format
            and double quotation marks. For example,
            ``"2023-04-21T11:30:00-04:00"``. You can use the greater
            than operator ``>`` to list messages that were created after
            a timestamp, or the less than operator ``<`` to list
            messages that were created before a timestamp. To filter
            messages within a time interval, use the ``AND`` operator
            between two timestamps.

            To filter by thread, specify the ``thread.name``, formatted
            as ``spaces/{space}/threads/{thread}``. You can only specify
            one ``thread.name`` per query.

            To filter by both thread and date, use the ``AND`` operator
            in your query.

            For example, the following queries are valid:

            ::

               create_time > "2012-04-21T11:30:00-04:00"

               create_time > "2012-04-21T11:30:00-04:00" AND
                 thread.name = spaces/AAAAAAAAAAA/threads/123

               create_time > "2012-04-21T11:30:00+00:00" AND

               create_time < "2013-01-01T00:00:00+00:00" AND
                 thread.name = spaces/AAAAAAAAAAA/threads/123

               thread.name = spaces/AAAAAAAAAAA/threads/123

            Invalid queries are rejected by the server with an
            ``INVALID_ARGUMENT`` error.
        order_by (str):
            Optional, if resuming from a previous query.

            How the list of messages is ordered. Specify a value to
            order by an ordering operation. Valid ordering operation
            values are as follows:

            -  ``ASC`` for ascending.

            -  ``DESC`` for descending.

            The default ordering is ``create_time ASC``.
        show_deleted (bool):
            Whether to include deleted messages. Deleted
            messages include deleted time and metadata about
            their deletion, but message content is
            unavailable.
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
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    show_deleted: bool = proto.Field(
        proto.BOOL,
        number=6,
    )


class ListMessagesResponse(proto.Message):
    r"""Response message for listing messages.

    Attributes:
        messages (MutableSequence[google.apps.chat_v1.types.Message]):
            List of messages.
        next_page_token (str):
            You can send a token as ``pageToken`` to retrieve the next
            page of results. If empty, there are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    messages: MutableSequence["Message"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Message",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class DialogAction(proto.Message):
    r"""Contains a
    `dialog <https://developers.google.com/workspace/chat/dialogs>`__
    and request status code.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        dialog (google.apps.chat_v1.types.Dialog):
            Input only.
            `Dialog <https://developers.google.com/workspace/chat/dialogs>`__
            for the request.

            This field is a member of `oneof`_ ``action``.
        action_status (google.apps.chat_v1.types.ActionStatus):
            Input only. Status for a request to either invoke or submit
            a
            `dialog <https://developers.google.com/workspace/chat/dialogs>`__.
            Displays a status and message to users, if necessary. For
            example, in case of an error or success.
    """

    dialog: "Dialog" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="action",
        message="Dialog",
    )
    action_status: gc_action_status.ActionStatus = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gc_action_status.ActionStatus,
    )


class Dialog(proto.Message):
    r"""Wrapper around the card body of the dialog.

    Attributes:
        body (google.apps.card_v1.types.Card):
            Input only. Body of the dialog, which is rendered in a
            modal. Google Chat apps don't support the following card
            entities: ``DateTimePicker``, ``OnChangeAction``.
    """

    body: gac_card.Card = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gac_card.Card,
    )


class CardWithId(proto.Message):
    r"""A
    `card <https://developers.google.com/workspace/chat/api/reference/rest/v1/cards>`__
    in a Google Chat message.

    Only Chat apps can create cards. If your Chat app `authenticates as
    a
    user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
    the message can't contain cards.

    `Card builder <https://addons.gsuite.google.com/uikit/builder>`__

    Attributes:
        card_id (str):
            Required if the message contains multiple
            cards. A unique identifier for a card in a
            message.
        card (google.apps.card_v1.types.Card):
            A card. Maximum size is 32 KB.
    """

    card_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    card: gac_card.Card = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gac_card.Card,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
