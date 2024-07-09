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
from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.apps.chat_v1.types import history_state

__protobuf__ = proto.module(
    package="google.chat.v1",
    manifest={
        "Space",
        "CreateSpaceRequest",
        "ListSpacesRequest",
        "ListSpacesResponse",
        "GetSpaceRequest",
        "FindDirectMessageRequest",
        "UpdateSpaceRequest",
        "DeleteSpaceRequest",
        "CompleteImportSpaceRequest",
        "CompleteImportSpaceResponse",
    },
)


class Space(proto.Message):
    r"""A space in Google Chat. Spaces are conversations between two
    or more users or 1:1 messages between a user and a Chat app.

    Attributes:
        name (str):
            Resource name of the space.

            Format: ``spaces/{space}``
        type_ (google.apps.chat_v1.types.Space.Type):
            Output only. Deprecated: Use ``space_type`` instead. The
            type of a space.
        space_type (google.apps.chat_v1.types.Space.SpaceType):
            The type of space. Required when creating a
            space or updating the space type of a space.
            Output only for other usage.
        single_user_bot_dm (bool):
            Optional. Whether the space is a DM between a
            Chat app and a single human.
        threaded (bool):
            Output only. Deprecated: Use ``spaceThreadingState``
            instead. Whether messages are threaded in this space.
        display_name (str):
            The space's display name. Required when `creating a
            space <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces/create>`__.
            If you receive the error message ``ALREADY_EXISTS`` when
            creating a space or updating the ``displayName``, try a
            different ``displayName``. An existing space within the
            Google Workspace organization might already use this display
            name.

            For direct messages, this field might be empty.

            Supports up to 128 characters.
        external_user_allowed (bool):
            Immutable. Whether this space permits any Google Chat user
            as a member. Input when creating a space in a Google
            Workspace organization. Omit this field when creating spaces
            in the following conditions:

            -  The authenticated user uses a consumer account (unmanaged
               user account). By default, a space created by a consumer
               account permits any Google Chat user.

            -  The space is used to [import data to Google Chat]
               (https://developers.google.com/chat/api/guides/import-data-overview)
               because import mode spaces must only permit members from
               the same Google Workspace organization. However, as part
               of the `Google Workspace Developer Preview
               Program <https://developers.google.com/workspace/preview>`__,
               import mode spaces can permit any Google Chat user so
               this field can then be set for import mode spaces.

            For existing spaces, this field is output only.
        space_threading_state (google.apps.chat_v1.types.Space.SpaceThreadingState):
            Output only. The threading state in the Chat
            space.
        space_details (google.apps.chat_v1.types.Space.SpaceDetails):
            Details about the space including description
            and rules.
        space_history_state (google.apps.chat_v1.types.HistoryState):
            The message history state for messages and
            threads in this space.
        import_mode (bool):
            Optional. Whether this space is created in ``Import Mode``
            as part of a data migration into Google Workspace. While
            spaces are being imported, they aren't visible to users
            until the import is complete.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Immutable. For spaces created in Chat, the time
            the space was created. This field is output only, except
            when used in import mode spaces.

            For import mode spaces, set this field to the historical
            timestamp at which the space was created in the source in
            order to preserve the original creation time.

            Only populated in the output when ``spaceType`` is
            ``GROUP_CHAT`` or ``SPACE``.
        admin_installed (bool):
            Output only. For direct message (DM) spaces
            with a Chat app, whether the space was created
            by a Google Workspace administrator.
            Administrators can install and set up a direct
            message with a Chat app on behalf of users in
            their organization.

            To support admin install, your Chat app must
            feature direct messaging.
        access_settings (google.apps.chat_v1.types.Space.AccessSettings):
            Optional. Specifies the `access
            setting <https://support.google.com/chat/answer/11971020>`__
            of the space. Only populated when the ``space_type`` is
            ``SPACE``.
        space_uri (str):
            Output only. The URI for a user to access the
            space.
    """

    class Type(proto.Enum):
        r"""Deprecated: Use ``SpaceType`` instead.

        Values:
            TYPE_UNSPECIFIED (0):
                Reserved.
            ROOM (1):
                Conversations between two or more humans.
            DM (2):
                1:1 Direct Message between a human and a Chat
                app, where all messages are flat. Note that this
                doesn't include direct messages between two
                humans.
        """
        TYPE_UNSPECIFIED = 0
        ROOM = 1
        DM = 2

    class SpaceType(proto.Enum):
        r"""The type of space. Required when creating or updating a
        space. Output only for other usage.

        Values:
            SPACE_TYPE_UNSPECIFIED (0):
                Reserved.
            SPACE (1):
                A place where people send messages, share files, and
                collaborate. A ``SPACE`` can include Chat apps.
            GROUP_CHAT (2):
                Group conversations between 3 or more people. A
                ``GROUP_CHAT`` can include Chat apps.
            DIRECT_MESSAGE (3):
                1:1 messages between two humans or a human
                and a Chat app.
        """
        SPACE_TYPE_UNSPECIFIED = 0
        SPACE = 1
        GROUP_CHAT = 2
        DIRECT_MESSAGE = 3

    class SpaceThreadingState(proto.Enum):
        r"""Specifies the type of threading state in the Chat space.

        Values:
            SPACE_THREADING_STATE_UNSPECIFIED (0):
                Reserved.
            THREADED_MESSAGES (2):
                Named spaces that support message threads.
                When users respond to a message, they can reply
                in-thread, which keeps their response in the
                context of the original message.
            GROUPED_MESSAGES (3):
                Named spaces where the conversation is
                organized by topic. Topics and their replies are
                grouped together.
            UNTHREADED_MESSAGES (4):
                Direct messages (DMs) between two people and
                group conversations between 3 or more people.
        """
        SPACE_THREADING_STATE_UNSPECIFIED = 0
        THREADED_MESSAGES = 2
        GROUPED_MESSAGES = 3
        UNTHREADED_MESSAGES = 4

    class SpaceDetails(proto.Message):
        r"""Details about the space including description and rules.

        Attributes:
            description (str):
                Optional. A description of the space. For
                example, describe the space's discussion topic,
                functional purpose, or participants.

                Supports up to 150 characters.
            guidelines (str):
                Optional. The space's rules, expectations,
                and etiquette.
                Supports up to 5,000 characters.
        """

        description: str = proto.Field(
            proto.STRING,
            number=1,
        )
        guidelines: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class AccessSettings(proto.Message):
        r"""Represents the `access
        setting <https://support.google.com/chat/answer/11971020>`__ of the
        space.

        Attributes:
            access_state (google.apps.chat_v1.types.Space.AccessSettings.AccessState):
                Output only. Indicates the access state of
                the space.
            audience (str):
                Optional. The resource name of the `target
                audience <https://support.google.com/a/answer/9934697>`__
                who can discover the space, join the space, and preview the
                messages in the space. For details, see `Make a space
                discoverable to a target
                audience <https://developers.google.com/workspace/chat/space-target-audience>`__.

                Format: ``audiences/{audience}``

                To use the default target audience for the Google Workspace
                organization, set to ``audiences/default``.
        """

        class AccessState(proto.Enum):
            r"""Represents the access state of the space.

            Values:
                ACCESS_STATE_UNSPECIFIED (0):
                    Access state is unknown or not supported in
                    this API.
                PRIVATE (1):
                    Space is discoverable by added or invited
                    members or groups.
                DISCOVERABLE (2):
                    Space is discoverable by the selected `target
                    audience <https://support.google.com/a/answer/9934697>`__,
                    as well as added or invited members or groups.
            """
            ACCESS_STATE_UNSPECIFIED = 0
            PRIVATE = 1
            DISCOVERABLE = 2

        access_state: "Space.AccessSettings.AccessState" = proto.Field(
            proto.ENUM,
            number=1,
            enum="Space.AccessSettings.AccessState",
        )
        audience: str = proto.Field(
            proto.STRING,
            number=3,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    type_: Type = proto.Field(
        proto.ENUM,
        number=2,
        enum=Type,
    )
    space_type: SpaceType = proto.Field(
        proto.ENUM,
        number=10,
        enum=SpaceType,
    )
    single_user_bot_dm: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    threaded: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    external_user_allowed: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    space_threading_state: SpaceThreadingState = proto.Field(
        proto.ENUM,
        number=9,
        enum=SpaceThreadingState,
    )
    space_details: SpaceDetails = proto.Field(
        proto.MESSAGE,
        number=11,
        message=SpaceDetails,
    )
    space_history_state: history_state.HistoryState = proto.Field(
        proto.ENUM,
        number=13,
        enum=history_state.HistoryState,
    )
    import_mode: bool = proto.Field(
        proto.BOOL,
        number=16,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=17,
        message=timestamp_pb2.Timestamp,
    )
    admin_installed: bool = proto.Field(
        proto.BOOL,
        number=19,
    )
    access_settings: AccessSettings = proto.Field(
        proto.MESSAGE,
        number=23,
        message=AccessSettings,
    )
    space_uri: str = proto.Field(
        proto.STRING,
        number=25,
    )


class CreateSpaceRequest(proto.Message):
    r"""A request to create a named space.

    Attributes:
        space (google.apps.chat_v1.types.Space):
            Required. The ``displayName`` and ``spaceType`` fields must
            be populated. Only ``SpaceType.SPACE`` is supported.

            If you receive the error message ``ALREADY_EXISTS`` when
            creating a space, try a different ``displayName``. An
            existing space within the Google Workspace organization
            might already use this display name.

            The space ``name`` is assigned on the server so anything
            specified in this field will be ignored.
        request_id (str):
            Optional. A unique identifier for this
            request. A random UUID is recommended.
            Specifying an existing request ID returns the
            space created with that ID instead of creating a
            new space.
            Specifying an existing request ID from the same
            Chat app with a different authenticated user
            returns an error.
    """

    space: "Space" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Space",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ListSpacesRequest(proto.Message):
    r"""A request to list the spaces the caller is a member of.

    Attributes:
        page_size (int):
            Optional. The maximum number of spaces to return. The
            service might return fewer than this value.

            If unspecified, at most 100 spaces are returned.

            The maximum value is 1000. If you use a value more than
            1000, it's automatically changed to 1000.

            Negative values return an ``INVALID_ARGUMENT`` error.
        page_token (str):
            Optional. A page token, received from a
            previous list spaces call. Provide this
            parameter to retrieve the subsequent page.

            When paginating, the filter value should match
            the call that provided the page token. Passing a
            different value may lead to unexpected results.
        filter (str):
            Optional. A query filter.

            You can filter spaces by the space type
            (```space_type`` <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces#spacetype>`__).

            To filter by space type, you must specify valid enum value,
            such as ``SPACE`` or ``GROUP_CHAT`` (the ``space_type``
            can't be ``SPACE_TYPE_UNSPECIFIED``). To query for multiple
            space types, use the ``OR`` operator.

            For example, the following queries are valid:

            ::

               space_type = "SPACE"
               spaceType = "GROUP_CHAT" OR spaceType = "DIRECT_MESSAGE"

            Invalid queries are rejected by the server with an
            ``INVALID_ARGUMENT`` error.
    """

    page_size: int = proto.Field(
        proto.INT32,
        number=1,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListSpacesResponse(proto.Message):
    r"""The response for a list spaces request.

    Attributes:
        spaces (MutableSequence[google.apps.chat_v1.types.Space]):
            List of spaces in the requested (or first)
            page.
        next_page_token (str):
            You can send a token as ``pageToken`` to retrieve the next
            page of results. If empty, there are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    spaces: MutableSequence["Space"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Space",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetSpaceRequest(proto.Message):
    r"""A request to return a single space.

    Attributes:
        name (str):
            Required. Resource name of the space, in the form
            ``spaces/{space}``.

            Format: ``spaces/{space}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class FindDirectMessageRequest(proto.Message):
    r"""A request to get direct message space based on the user
    resource.

    Attributes:
        name (str):
            Required. Resource name of the user to find direct message
            with.

            Format: ``users/{user}``, where ``{user}`` is either the
            ``id`` for the
            `person <https://developers.google.com/people/api/rest/v1/people>`__
            from the People API, or the ``id`` for the
            `user <https://developers.google.com/admin-sdk/directory/reference/rest/v1/users>`__
            in the Directory API. For example, if the People API profile
            ID is ``123456789``, you can find a direct message with that
            person by using ``users/123456789`` as the ``name``. When
            `authenticated as a
            user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
            you can use the email as an alias for ``{user}``. For
            example, ``users/example@gmail.com`` where
            ``example@gmail.com`` is the email of the Google Chat user.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateSpaceRequest(proto.Message):
    r"""A request to update a single space.

    Attributes:
        space (google.apps.chat_v1.types.Space):
            Required. Space with fields to be updated. ``Space.name``
            must be populated in the form of ``spaces/{space}``. Only
            fields specified by ``update_mask`` are updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The updated field paths, comma separated if there
            are multiple.

            Currently supported field paths:

            -  ``display_name`` (Only supports changing the display name
               of a space with the ``SPACE`` type, or when also
               including the ``space_type`` mask to change a
               ``GROUP_CHAT`` space type to ``SPACE``. Trying to update
               the display name of a ``GROUP_CHAT`` or a
               ``DIRECT_MESSAGE`` space results in an invalid argument
               error. If you receive the error message
               ``ALREADY_EXISTS`` when updating the ``displayName``, try
               a different ``displayName``. An existing space within the
               Google Workspace organization might already use this
               display name.)

            -  ``space_type`` (Only supports changing a ``GROUP_CHAT``
               space type to ``SPACE``. Include ``display_name``
               together with ``space_type`` in the update mask and
               ensure that the specified space has a non-empty display
               name and the ``SPACE`` space type. Including the
               ``space_type`` mask and the ``SPACE`` type in the
               specified space when updating the display name is
               optional if the existing space already has the ``SPACE``
               type. Trying to update the space type in other ways
               results in an invalid argument error). ``space_type`` is
               not supported with admin access.

            -  ``space_details``

            -  ``space_history_state`` (Supports `turning history on or
               off for the
               space <https://support.google.com/chat/answer/7664687>`__
               if `the organization allows users to change their history
               setting <https://support.google.com/a/answer/7664184>`__.
               Warning: mutually exclusive with all other field paths.)
               ``space_history_state`` is not supported with admin
               access.

            -  ``access_settings.audience`` (Supports changing the
               `access
               setting <https://support.google.com/chat/answer/11971020>`__
               of who can discover the space, join the space, and
               preview the messages in space. If no audience is
               specified in the access setting, the space's access
               setting is updated to private. Warning: mutually
               exclusive with all other field paths.)
               ``access_settings.audience`` is not supported with admin
               access.

            -  Developer Preview: Supports changing the `permission
               settings <https://support.google.com/chat/answer/13340792>`__
               of a space, supported field paths include:
               ``permission_settings.manage_members_and_groups``,
               ``permission_settings.modify_space_details``,
               ``permission_settings.toggle_history``,
               ``permission_settings.use_at_mention_all``,
               ``permission_settings.manage_apps``,
               ``permission_settings.manage_webhooks``,
               ``permission_settings.reply_messages`` (Warning: mutually
               exclusive with all other non-permission settings field
               paths). ``permission_settings`` is not supported with
               admin access.
    """

    space: "Space" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Space",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class DeleteSpaceRequest(proto.Message):
    r"""Request for deleting a space.

    Attributes:
        name (str):
            Required. Resource name of the space to delete.

            Format: ``spaces/{space}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CompleteImportSpaceRequest(proto.Message):
    r"""Request message for completing the import process for a
    space.

    Attributes:
        name (str):
            Required. Resource name of the import mode space.

            Format: ``spaces/{space}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CompleteImportSpaceResponse(proto.Message):
    r"""Response message for completing the import process for a
    space.

    Attributes:
        space (google.apps.chat_v1.types.Space):
            The import mode space.
    """

    space: "Space" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Space",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
