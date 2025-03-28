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
        "SearchSpacesRequest",
        "SearchSpacesResponse",
        "DeleteSpaceRequest",
        "CompleteImportSpaceRequest",
        "CompleteImportSpaceResponse",
    },
)


class Space(proto.Message):
    r"""A space in Google Chat. Spaces are conversations between two
    or more users or 1:1 messages between a user and a Chat app.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Identifier. Resource name of the space.

            Format: ``spaces/{space}``

            Where ``{space}`` represents the system-assigned ID for the
            space. You can obtain the space ID by calling the
            ```spaces.list()`` <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces/list>`__
            method or from the space URL. For example, if the space URL
            is
            ``https://mail.google.com/mail/u/0/#chat/space/AAAAAAAAA``,
            the space ID is ``AAAAAAAAA``.
        type_ (google.apps.chat_v1.types.Space.Type):
            Output only. Deprecated: Use ``space_type`` instead. The
            type of a space.
        space_type (google.apps.chat_v1.types.Space.SpaceType):
            Optional. The type of space. Required when
            creating a space or updating the space type of a
            space. Output only for other usage.
        single_user_bot_dm (bool):
            Optional. Whether the space is a DM between a
            Chat app and a single human.
        threaded (bool):
            Output only. Deprecated: Use ``spaceThreadingState``
            instead. Whether messages are threaded in this space.
        display_name (str):
            Optional. The space's display name. Required when `creating
            a
            space <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces/create>`__
            with a ``spaceType`` of ``SPACE``. If you receive the error
            message ``ALREADY_EXISTS`` when creating a space or updating
            the ``displayName``, try a different ``displayName``. An
            existing space within the Google Workspace organization
            might already use this display name.

            For direct messages, this field might be empty.

            Supports up to 128 characters.
        external_user_allowed (bool):
            Optional. Immutable. Whether this space permits any Google
            Chat user as a member. Input when creating a space in a
            Google Workspace organization. Omit this field when creating
            spaces in the following conditions:

            -  The authenticated user uses a consumer account (unmanaged
               user account). By default, a space created by a consumer
               account permits any Google Chat user.

            For existing spaces, this field is output only.
        space_threading_state (google.apps.chat_v1.types.Space.SpaceThreadingState):
            Output only. The threading state in the Chat
            space.
        space_details (google.apps.chat_v1.types.Space.SpaceDetails):
            Optional. Details about the space including
            description and rules.
        space_history_state (google.apps.chat_v1.types.HistoryState):
            Optional. The message history state for
            messages and threads in this space.
        import_mode (bool):
            Optional. Whether this space is created in ``Import Mode``
            as part of a data migration into Google Workspace. While
            spaces are being imported, they aren't visible to users
            until the import is complete.

            Creating a space in ``Import Mode``\ requires `user
            authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Immutable. For spaces created in Chat, the time
            the space was created. This field is output only, except
            when used in import mode spaces.

            For import mode spaces, set this field to the historical
            timestamp at which the space was created in the source in
            order to preserve the original creation time.

            Only populated in the output when ``spaceType`` is
            ``GROUP_CHAT`` or ``SPACE``.
        last_active_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp of the last message in
            the space.
        admin_installed (bool):
            Output only. For direct message (DM) spaces
            with a Chat app, whether the space was created
            by a Google Workspace administrator.
            Administrators can install and set up a direct
            message with a Chat app on behalf of users in
            their organization.

            To support admin install, your Chat app must
            feature direct messaging.
        membership_count (google.apps.chat_v1.types.Space.MembershipCount):
            Output only. The count of joined memberships grouped by
            member type. Populated when the ``space_type`` is ``SPACE``,
            ``DIRECT_MESSAGE`` or ``GROUP_CHAT``.
        access_settings (google.apps.chat_v1.types.Space.AccessSettings):
            Optional. Specifies the `access
            setting <https://support.google.com/chat/answer/11971020>`__
            of the space. Only populated when the ``space_type`` is
            ``SPACE``.
        space_uri (str):
            Output only. The URI for a user to access the
            space.
        predefined_permission_settings (google.apps.chat_v1.types.Space.PredefinedPermissionSettings):
            Optional. Input only. Predefined space permission settings,
            input only when creating a space. If the field is not set, a
            collaboration space is created. After you create the space,
            settings are populated in the ``PermissionSettings`` field.

            This field is a member of `oneof`_ ``space_permission_settings``.
        permission_settings (google.apps.chat_v1.types.Space.PermissionSettings):
            Optional. Space permission settings for
            existing spaces. Input for updating exact space
            permission settings, where existing permission
            settings are replaced. Output lists current
            permission settings.

            This field is a member of `oneof`_ ``space_permission_settings``.
        import_mode_expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the space will be automatically
            deleted by the system if it remains in import mode.

            Each space created in import mode must exit this mode before
            this expire time using ``spaces.completeImport``.

            This field is only populated for spaces that were created
            with import mode.
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

    class PredefinedPermissionSettings(proto.Enum):
        r"""Predefined permission settings that you can only specify when
        creating a named space. More settings might be added in the future.
        For details about permission settings for named spaces, see `Learn
        about spaces <https://support.google.com/chat/answer/7659784>`__.

        Values:
            PREDEFINED_PERMISSION_SETTINGS_UNSPECIFIED (0):
                Unspecified. Don't use.
            COLLABORATION_SPACE (1):
                Setting to make the space a collaboration
                space where all members can post messages.
            ANNOUNCEMENT_SPACE (2):
                Setting to make the space an announcement
                space where only space managers can post
                messages.
        """
        PREDEFINED_PERMISSION_SETTINGS_UNSPECIFIED = 0
        COLLABORATION_SPACE = 1
        ANNOUNCEMENT_SPACE = 2

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

    class MembershipCount(proto.Message):
        r"""Represents the count of memberships of a space, grouped into
        categories.

        Attributes:
            joined_direct_human_user_count (int):
                Output only. Count of human users that have
                directly joined the space, not counting users
                joined by having membership in a joined group.
            joined_group_count (int):
                Output only. Count of all groups that have
                directly joined the space.
        """

        joined_direct_human_user_count: int = proto.Field(
            proto.INT32,
            number=4,
        )
        joined_group_count: int = proto.Field(
            proto.INT32,
            number=5,
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
                messages in the space. If unset, only users or Google Groups
                who have been individually invited or added to the space can
                access it. For details, see `Make a space discoverable to a
                target
                audience <https://developers.google.com/workspace/chat/space-target-audience>`__.

                Format: ``audiences/{audience}``

                To use the default target audience for the Google Workspace
                organization, set to ``audiences/default``.

                Reading the target audience supports:

                -  `User
                   authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__

                -  `App
                   authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__
                   with `administrator
                   approval <https://support.google.com/a?p=chat-app-auth>`__
                   with the ``chat.app.spaces`` scope in `Developer
                   Preview <https://developers.google.com/workspace/preview>`__.

                This field is not populated when using the ``chat.bot``
                scope with `app
                authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-app>`__.

                Setting the target audience requires `user
                authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.
        """

        class AccessState(proto.Enum):
            r"""Represents the access state of the space.

            Values:
                ACCESS_STATE_UNSPECIFIED (0):
                    Access state is unknown or not supported in
                    this API.
                PRIVATE (1):
                    Only users or Google Groups that have been
                    individually added or invited by other users or
                    Google Workspace administrators can discover and
                    access the space.
                DISCOVERABLE (2):
                    A space manager has granted a target audience access to the
                    space. Users or Google Groups that have been individually
                    added or invited to the space can also discover and access
                    the space. To learn more, see `Make a space discoverable to
                    specific
                    users <https://developers.google.com/workspace/chat/space-target-audience>`__.

                    Creating discoverable spaces requires `user
                    authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.
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

    class PermissionSettings(proto.Message):
        r"""`Permission
        settings <https://support.google.com/chat/answer/13340792>`__ that
        you can specify when updating an existing named space.

        To set permission settings when creating a space, specify the
        ``PredefinedPermissionSettings`` field in your request.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            manage_members_and_groups (google.apps.chat_v1.types.Space.PermissionSetting):
                Optional. Setting for managing members and
                groups in a space.

                This field is a member of `oneof`_ ``_manage_members_and_groups``.
            modify_space_details (google.apps.chat_v1.types.Space.PermissionSetting):
                Optional. Setting for updating space name,
                avatar, description and guidelines.

                This field is a member of `oneof`_ ``_modify_space_details``.
            toggle_history (google.apps.chat_v1.types.Space.PermissionSetting):
                Optional. Setting for toggling space history
                on and off.

                This field is a member of `oneof`_ ``_toggle_history``.
            use_at_mention_all (google.apps.chat_v1.types.Space.PermissionSetting):
                Optional. Setting for using @all in a space.

                This field is a member of `oneof`_ ``_use_at_mention_all``.
            manage_apps (google.apps.chat_v1.types.Space.PermissionSetting):
                Optional. Setting for managing apps in a
                space.

                This field is a member of `oneof`_ ``_manage_apps``.
            manage_webhooks (google.apps.chat_v1.types.Space.PermissionSetting):
                Optional. Setting for managing webhooks in a
                space.

                This field is a member of `oneof`_ ``_manage_webhooks``.
            post_messages (google.apps.chat_v1.types.Space.PermissionSetting):
                Output only. Setting for posting messages in
                a space.

                This field is a member of `oneof`_ ``_post_messages``.
            reply_messages (google.apps.chat_v1.types.Space.PermissionSetting):
                Optional. Setting for replying to messages in
                a space.

                This field is a member of `oneof`_ ``_reply_messages``.
        """

        manage_members_and_groups: "Space.PermissionSetting" = proto.Field(
            proto.MESSAGE,
            number=1,
            optional=True,
            message="Space.PermissionSetting",
        )
        modify_space_details: "Space.PermissionSetting" = proto.Field(
            proto.MESSAGE,
            number=2,
            optional=True,
            message="Space.PermissionSetting",
        )
        toggle_history: "Space.PermissionSetting" = proto.Field(
            proto.MESSAGE,
            number=3,
            optional=True,
            message="Space.PermissionSetting",
        )
        use_at_mention_all: "Space.PermissionSetting" = proto.Field(
            proto.MESSAGE,
            number=4,
            optional=True,
            message="Space.PermissionSetting",
        )
        manage_apps: "Space.PermissionSetting" = proto.Field(
            proto.MESSAGE,
            number=5,
            optional=True,
            message="Space.PermissionSetting",
        )
        manage_webhooks: "Space.PermissionSetting" = proto.Field(
            proto.MESSAGE,
            number=6,
            optional=True,
            message="Space.PermissionSetting",
        )
        post_messages: "Space.PermissionSetting" = proto.Field(
            proto.MESSAGE,
            number=7,
            optional=True,
            message="Space.PermissionSetting",
        )
        reply_messages: "Space.PermissionSetting" = proto.Field(
            proto.MESSAGE,
            number=8,
            optional=True,
            message="Space.PermissionSetting",
        )

    class PermissionSetting(proto.Message):
        r"""Represents a space permission setting.

        Attributes:
            managers_allowed (bool):
                Optional. Whether spaces managers have this
                permission.
            members_allowed (bool):
                Optional. Whether non-manager members have
                this permission.
        """

        managers_allowed: bool = proto.Field(
            proto.BOOL,
            number=1,
        )
        members_allowed: bool = proto.Field(
            proto.BOOL,
            number=2,
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
    last_active_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=18,
        message=timestamp_pb2.Timestamp,
    )
    admin_installed: bool = proto.Field(
        proto.BOOL,
        number=19,
    )
    membership_count: MembershipCount = proto.Field(
        proto.MESSAGE,
        number=20,
        message=MembershipCount,
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
    predefined_permission_settings: PredefinedPermissionSettings = proto.Field(
        proto.ENUM,
        number=26,
        oneof="space_permission_settings",
        enum=PredefinedPermissionSettings,
    )
    permission_settings: PermissionSettings = proto.Field(
        proto.MESSAGE,
        number=27,
        oneof="space_permission_settings",
        message=PermissionSettings,
    )
    import_mode_expire_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=28,
        message=timestamp_pb2.Timestamp,
    )


class CreateSpaceRequest(proto.Message):
    r"""A request to create a named space with no members.

    Attributes:
        space (google.apps.chat_v1.types.Space):
            Required. The ``displayName`` and ``spaceType`` fields must
            be populated. Only ``SpaceType.SPACE`` and
            ``SpaceType.GROUP_CHAT`` are supported.
            ``SpaceType.GROUP_CHAT`` can only be used if ``importMode``
            is set to true.

            If you receive the error message ``ALREADY_EXISTS``, try a
            different ``displayName``. An existing space within the
            Google Workspace organization might already use this display
            name.

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
            List of spaces in the requested (or first) page. Note: The
            ``permissionSettings`` field is not returned in the Space
            object for list requests.
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
        use_admin_access (bool):
            Optional. When ``true``, the method runs using the user's
            Google Workspace administrator privileges.

            The calling user must be a Google Workspace administrator
            with the `manage chat and spaces conversations
            privilege <https://support.google.com/a/answer/13369245>`__.

            Requires the ``chat.admin.spaces`` or
            ``chat.admin.spaces.readonly`` `OAuth 2.0
            scopes <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    use_admin_access: bool = proto.Field(
        proto.BOOL,
        number=2,
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

            You can update the following fields for a space:

            ``space_details``: Updates the space's description. Supports
            up to 150 characters.

            ``display_name``: Only supports updating the display name
            for spaces where ``spaceType`` field is ``SPACE``. If you
            receive the error message ``ALREADY_EXISTS``, try a
            different value. An existing space within the Google
            Workspace organization might already use this display name.

            ``space_type``: Only supports changing a ``GROUP_CHAT``
            space type to ``SPACE``. Include ``display_name`` together
            with ``space_type`` in the update mask and ensure that the
            specified space has a non-empty display name and the
            ``SPACE`` space type. Including the ``space_type`` mask and
            the ``SPACE`` type in the specified space when updating the
            display name is optional if the existing space already has
            the ``SPACE`` type. Trying to update the space type in other
            ways results in an invalid argument error. ``space_type`` is
            not supported with ``useAdminAccess``.

            ``space_history_state``: Updates `space history
            settings <https://support.google.com/chat/answer/7664687>`__
            by turning history on or off for the space. Only supported
            if history settings are enabled for the Google Workspace
            organization. To update the space history state, you must
            omit all other field masks in your request.
            ``space_history_state`` is not supported with
            ``useAdminAccess``.

            ``access_settings.audience``: Updates the `access
            setting <https://support.google.com/chat/answer/11971020>`__
            of who can discover the space, join the space, and preview
            the messages in named space where ``spaceType`` field is
            ``SPACE``. If the existing space has a target audience, you
            can remove the audience and restrict space access by
            omitting a value for this field mask. To update access
            settings for a space, the authenticating user must be a
            space manager and omit all other field masks in your
            request. You can't update this field if the space is in
            `import
            mode <https://developers.google.com/workspace/chat/import-data-overview>`__.
            To learn more, see `Make a space discoverable to specific
            users <https://developers.google.com/workspace/chat/space-target-audience>`__.
            ``access_settings.audience`` is not supported with
            ``useAdminAccess``.

            ``permission_settings``: Supports changing the `permission
            settings <https://support.google.com/chat/answer/13340792>`__
            of a space. When updating permission settings, you can only
            specify ``permissionSettings`` field masks; you cannot
            update other field masks at the same time.
            ``permissionSettings`` is not supported with
            ``useAdminAccess``. The supported field masks include:

            -  ``permission_settings.manageMembersAndGroups``
            -  ``permission_settings.modifySpaceDetails``
            -  ``permission_settings.toggleHistory``
            -  ``permission_settings.useAtMentionAll``
            -  ``permission_settings.manageApps``
            -  ``permission_settings.manageWebhooks``
            -  ``permission_settings.replyMessages``
        use_admin_access (bool):
            Optional. When ``true``, the method runs using the user's
            Google Workspace administrator privileges.

            The calling user must be a Google Workspace administrator
            with the `manage chat and spaces conversations
            privilege <https://support.google.com/a/answer/13369245>`__.

            Requires the ``chat.admin.spaces`` `OAuth 2.0
            scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__.

            Some ``FieldMask`` values are not supported using admin
            access. For details, see the description of ``update_mask``.
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
    use_admin_access: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class SearchSpacesRequest(proto.Message):
    r"""Request to search for a list of spaces based on a query.

    Attributes:
        use_admin_access (bool):
            When ``true``, the method runs using the user's Google
            Workspace administrator privileges.

            The calling user must be a Google Workspace administrator
            with the `manage chat and spaces conversations
            privilege <https://support.google.com/a/answer/13369245>`__.

            Requires either the ``chat.admin.spaces.readonly`` or
            ``chat.admin.spaces`` `OAuth 2.0
            scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__.

            This method currently only supports admin access, thus only
            ``true`` is accepted for this field.
        page_size (int):
            The maximum number of spaces to return. The
            service may return fewer than this value.

            If unspecified, at most 100 spaces are returned.

            The maximum value is 1000. If you use a value
            more than 1000, it's automatically changed to
            1000.
        page_token (str):
            A token, received from the previous search
            spaces call. Provide this parameter to retrieve
            the subsequent page.

            When paginating, all other parameters provided
            should match the call that provided the page
            token. Passing different values to the other
            parameters might lead to unexpected results.
        query (str):
            Required. A search query.

            You can search by using the following parameters:

            -  ``create_time``
            -  ``customer``
            -  ``display_name``
            -  ``external_user_allowed``
            -  ``last_active_time``
            -  ``space_history_state``
            -  ``space_type``

            ``create_time`` and ``last_active_time`` accept a timestamp
            in `RFC-3339 <https://www.rfc-editor.org/rfc/rfc3339>`__
            format and the supported comparison operators are: ``=``,
            ``<``, ``>``, ``<=``, ``>=``.

            ``customer`` is required and is used to indicate which
            customer to fetch spaces from. ``customers/my_customer`` is
            the only supported value.

            ``display_name`` only accepts the ``HAS`` (``:``) operator.
            The text to match is first tokenized into tokens and each
            token is prefix-matched case-insensitively and independently
            as a substring anywhere in the space's ``display_name``. For
            example, ``Fun Eve`` matches ``Fun event`` or
            ``The evening was fun``, but not ``notFun event`` or
            ``even``.

            ``external_user_allowed`` accepts either ``true`` or
            ``false``.

            ``space_history_state`` only accepts values from the
            [``historyState``]
            (https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces#Space.HistoryState)
            field of a ``space`` resource.

            ``space_type`` is required and the only valid value is
            ``SPACE``.

            Across different fields, only ``AND`` operators are
            supported. A valid example is
            ``space_type = "SPACE" AND display_name:"Hello"`` and an
            invalid example is
            ``space_type = "SPACE" OR display_name:"Hello"``.

            Among the same field, ``space_type`` doesn't support ``AND``
            or ``OR`` operators. ``display_name``,
            'space_history_state', and 'external_user_allowed' only
            support ``OR`` operators. ``last_active_time`` and
            ``create_time`` support both ``AND`` and ``OR`` operators.
            ``AND`` can only be used to represent an interval, such as
            ``last_active_time < "2022-01-01T00:00:00+00:00" AND last_active_time > "2023-01-01T00:00:00+00:00"``.

            The following example queries are valid:

            ::

               customer = "customers/my_customer" AND space_type = "SPACE"

               customer = "customers/my_customer" AND space_type = "SPACE" AND
               display_name:"Hello World"

               customer = "customers/my_customer" AND space_type = "SPACE" AND
               (last_active_time < "2020-01-01T00:00:00+00:00" OR last_active_time >
               "2022-01-01T00:00:00+00:00")

               customer = "customers/my_customer" AND space_type = "SPACE" AND
               (display_name:"Hello World" OR display_name:"Fun event") AND
               (last_active_time > "2020-01-01T00:00:00+00:00" AND last_active_time <
               "2022-01-01T00:00:00+00:00")

               customer = "customers/my_customer" AND space_type = "SPACE" AND
               (create_time > "2019-01-01T00:00:00+00:00" AND create_time <
               "2020-01-01T00:00:00+00:00") AND (external_user_allowed = "true") AND
               (space_history_state = "HISTORY_ON" OR space_history_state = "HISTORY_OFF")
        order_by (str):
            Optional. How the list of spaces is ordered.

            Supported attributes to order by are:

            -  ``membership_count.joined_direct_human_user_count`` —
               Denotes the count of human users that have directly
               joined a space.
            -  ``last_active_time`` — Denotes the time when last
               eligible item is added to any topic of this space.
            -  ``create_time`` — Denotes the time of the space creation.

            Valid ordering operation values are:

            -  ``ASC`` for ascending. Default value.

            -  ``DESC`` for descending.

            The supported syntax are:

            -  ``membership_count.joined_direct_human_user_count DESC``
            -  ``membership_count.joined_direct_human_user_count ASC``
            -  ``last_active_time DESC``
            -  ``last_active_time ASC``
            -  ``create_time DESC``
            -  ``create_time ASC``
    """

    use_admin_access: bool = proto.Field(
        proto.BOOL,
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
    query: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )


class SearchSpacesResponse(proto.Message):
    r"""Response with a list of spaces corresponding to the search
    spaces request.

    Attributes:
        spaces (MutableSequence[google.apps.chat_v1.types.Space]):
            A page of the requested spaces.
        next_page_token (str):
            A token that can be used to retrieve the next
            page. If this field is empty, there are no
            subsequent pages.
        total_size (int):
            The total number of spaces that match the
            query, across all pages. If the result is over
            10,000 spaces, this value is an estimate.
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
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


class DeleteSpaceRequest(proto.Message):
    r"""Request for deleting a space.

    Attributes:
        name (str):
            Required. Resource name of the space to delete.

            Format: ``spaces/{space}``
        use_admin_access (bool):
            Optional. When ``true``, the method runs using the user's
            Google Workspace administrator privileges.

            The calling user must be a Google Workspace administrator
            with the `manage chat and spaces conversations
            privilege <https://support.google.com/a/answer/13369245>`__.

            Requires the ``chat.admin.delete`` `OAuth 2.0
            scope <https://developers.google.com/workspace/chat/authenticate-authorize#chat-api-scopes>`__.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    use_admin_access: bool = proto.Field(
        proto.BOOL,
        number=2,
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
