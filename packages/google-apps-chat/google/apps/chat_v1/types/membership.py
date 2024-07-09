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

from google.apps.chat_v1.types import group, user

__protobuf__ = proto.module(
    package="google.chat.v1",
    manifest={
        "Membership",
        "CreateMembershipRequest",
        "UpdateMembershipRequest",
        "ListMembershipsRequest",
        "ListMembershipsResponse",
        "GetMembershipRequest",
        "DeleteMembershipRequest",
    },
)


class Membership(proto.Message):
    r"""Represents a membership relation in Google Chat, such as
    whether a user or Chat app is invited to, part of, or absent
    from a space.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Resource name of the membership, assigned by the server.

            Format: ``spaces/{space}/members/{member}``
        state (google.apps.chat_v1.types.Membership.MembershipState):
            Output only. State of the membership.
        role (google.apps.chat_v1.types.Membership.MembershipRole):
            Optional. User's role within a Chat space, which determines
            their permitted actions in the space.

            This field can only be used as input in
            ``UpdateMembership``.
        member (google.apps.chat_v1.types.User):
            The Google Chat user or app the membership corresponds to.
            If your Chat app `authenticates as a
            user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
            the output populates the
            `user <https://developers.google.com/workspace/chat/api/reference/rest/v1/User>`__
            ``name`` and ``type``.

            This field is a member of `oneof`_ ``memberType``.
        group_member (google.apps.chat_v1.types.Group):
            The Google Group the membership corresponds
            to.

            This field is a member of `oneof`_ ``memberType``.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Immutable. The creation time of the
            membership, such as when a member joined or was
            invited to join a space. This field is output
            only, except when used to import historical
            memberships in import mode spaces.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. Immutable. The deletion time of the
            membership, such as when a member left or was
            removed from a space. This field is output only,
            except when used to import historical
            memberships in import mode spaces.
    """

    class MembershipState(proto.Enum):
        r"""Specifies the member's relationship with a space. Other
        membership states might be supported in the future.

        Values:
            MEMBERSHIP_STATE_UNSPECIFIED (0):
                Default value. Don't use.
            JOINED (1):
                The user is added to the space, and can
                participate in the space.
            INVITED (2):
                The user is invited to join the space, but
                hasn't joined it.
            NOT_A_MEMBER (3):
                The user doesn't belong to the space and
                doesn't have a pending invitation to join the
                space.
        """
        MEMBERSHIP_STATE_UNSPECIFIED = 0
        JOINED = 1
        INVITED = 2
        NOT_A_MEMBER = 3

    class MembershipRole(proto.Enum):
        r"""Represents a user's permitted actions in a Chat space. More
        enum values might be added in the future.

        Values:
            MEMBERSHIP_ROLE_UNSPECIFIED (0):
                Default value. For
                [users][google.chat.v1.Membership.member]: they aren't a
                member of the space, but can be invited. For [Google
                Groups][google.chat.v1.Membership.group_member]: they're
                always assigned this role (other enum values might be used
                in the future).
            ROLE_MEMBER (1):
                A member of the space. The user has basic
                permissions, like sending messages to the space.
                In 1:1 and unnamed group conversations, everyone
                has this role.
            ROLE_MANAGER (2):
                A space manager. The user has all basic permissions plus
                administrative permissions that let them manage the space,
                like adding or removing members. Only supported in
                [SpaceType.SPACE][google.chat.v1.Space.SpaceType].
        """
        MEMBERSHIP_ROLE_UNSPECIFIED = 0
        ROLE_MEMBER = 1
        ROLE_MANAGER = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: MembershipState = proto.Field(
        proto.ENUM,
        number=2,
        enum=MembershipState,
    )
    role: MembershipRole = proto.Field(
        proto.ENUM,
        number=7,
        enum=MembershipRole,
    )
    member: user.User = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="memberType",
        message=user.User,
    )
    group_member: group.Group = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="memberType",
        message=group.Group,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    delete_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )


class CreateMembershipRequest(proto.Message):
    r"""Request message for creating a membership.

    Attributes:
        parent (str):
            Required. The resource name of the space for
            which to create the membership.

            Format: spaces/{space}
        membership (google.apps.chat_v1.types.Membership):
            Required. The membership relation to create. The
            ``memberType`` field must contain a user with the
            ``user.name`` and ``user.type`` fields populated. The server
            will assign a resource name and overwrite anything
            specified. When a Chat app creates a membership relation for
            a human user, it must use the ``chat.memberships`` scope,
            set ``user.type`` to ``HUMAN``, and set ``user.name`` with
            format ``users/{user}``, where ``{user}`` can be the email
            address for the user. For users in the same Workspace
            organization ``{user}`` can also be the ``id`` of the
            `person <https://developers.google.com/people/api/rest/v1/people>`__
            from the People API, or the ``id`` for the user in the
            Directory API. For example, if the People API Person profile
            ID for ``user@example.com`` is ``123456789``, you can add
            the user to the space by setting the
            ``membership.member.name`` to ``users/user@example.com`` or
            ``users/123456789``. When a Chat app creates a membership
            relation for itself, it must use the
            ``chat.memberships.app`` scope, set ``user.type`` to
            ``BOT``, and set ``user.name`` to ``users/app``.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    membership: "Membership" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Membership",
    )


class UpdateMembershipRequest(proto.Message):
    r"""Request message for updating a membership.

    Attributes:
        membership (google.apps.chat_v1.types.Membership):
            Required. The membership to update. Only fields specified by
            ``update_mask`` are updated.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The field paths to update. Separate multiple
            values with commas or use ``*`` to update all field paths.

            Currently supported field paths:

            -  ``role``
    """

    membership: "Membership" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Membership",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class ListMembershipsRequest(proto.Message):
    r"""Request message for listing memberships.

    Attributes:
        parent (str):
            Required. The resource name of the space for
            which to fetch a membership list.

            Format: spaces/{space}
        page_size (int):
            Optional. The maximum number of memberships to return. The
            service might return fewer than this value.

            If unspecified, at most 100 memberships are returned.

            The maximum value is 1000. If you use a value more than
            1000, it's automatically changed to 1000.

            Negative values return an ``INVALID_ARGUMENT`` error.
        page_token (str):
            Optional. A page token, received from a
            previous call to list memberships. Provide this
            parameter to retrieve the subsequent page.

            When paginating, all other parameters provided
            should match the call that provided the page
            token. Passing different values to the other
            parameters might lead to unexpected results.
        filter (str):
            Optional. A query filter.

            You can filter memberships by a member's role
            (```role`` <https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.members#membershiprole>`__)
            and type
            (```member.type`` <https://developers.google.com/workspace/chat/api/reference/rest/v1/User#type>`__).

            To filter by role, set ``role`` to ``ROLE_MEMBER`` or
            ``ROLE_MANAGER``.

            To filter by type, set ``member.type`` to ``HUMAN`` or
            ``BOT``. Developer Preview: You can also filter for
            ``member.type`` using the ``!=`` operator.

            To filter by both role and type, use the ``AND`` operator.
            To filter by either role or type, use the ``OR`` operator.

            Either ``member.type = "HUMAN"`` or ``member.type != "BOT"``
            is required when ``use_admin_access`` is set to true. Other
            member type filters will be rejected.

            For example, the following queries are valid:

            ::

               role = "ROLE_MANAGER" OR role = "ROLE_MEMBER"
               member.type = "HUMAN" AND role = "ROLE_MANAGER"

               member.type != "BOT"

            The following queries are invalid:

            ::

               member.type = "HUMAN" AND member.type = "BOT"
               role = "ROLE_MANAGER" AND role = "ROLE_MEMBER"

            Invalid queries are rejected by the server with an
            ``INVALID_ARGUMENT`` error.
        show_groups (bool):
            Optional. When ``true``, also returns memberships associated
            with a [Google
            Group][google.chat.v1.Membership.group_member], in addition
            to other types of memberships. If a
            [filter][google.chat.v1.ListMembershipsRequest.filter] is
            set, [Google Group][google.chat.v1.Membership.group_member]
            memberships that don't match the filter criteria aren't
            returned.
        show_invited (bool):
            Optional. When ``true``, also returns memberships associated
            with
            [invited][google.chat.v1.Membership.MembershipState.INVITED]
            members, in addition to other types of memberships. If a
            filter is set,
            [invited][google.chat.v1.Membership.MembershipState.INVITED]
            memberships that don't match the filter criteria aren't
            returned.

            Currently requires `user
            authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__.
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
        number=5,
    )
    show_groups: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    show_invited: bool = proto.Field(
        proto.BOOL,
        number=7,
    )


class ListMembershipsResponse(proto.Message):
    r"""Response to list memberships of the space.

    Attributes:
        memberships (MutableSequence[google.apps.chat_v1.types.Membership]):
            Unordered list. List of memberships in the
            requested (or first) page.
        next_page_token (str):
            A token that you can send as ``pageToken`` to retrieve the
            next page of results. If empty, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    memberships: MutableSequence["Membership"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Membership",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetMembershipRequest(proto.Message):
    r"""Request to get a membership of a space.

    Attributes:
        name (str):
            Required. Resource name of the membership to retrieve.

            To get the app's own membership `by using user
            authentication <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
            you can optionally use ``spaces/{space}/members/app``.

            Format: ``spaces/{space}/members/{member}`` or
            ``spaces/{space}/members/app``

            When `authenticated as a
            user <https://developers.google.com/workspace/chat/authenticate-authorize-chat-user>`__,
            you can use the user's email as an alias for ``{member}``.
            For example, ``spaces/{space}/members/example@gmail.com``
            where ``example@gmail.com`` is the email of the Google Chat
            user.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class DeleteMembershipRequest(proto.Message):
    r"""Request to delete a membership in a space.

    Attributes:
        name (str):
            Required. Resource name of the membership to delete. Chat
            apps can delete human users' or their own memberships. Chat
            apps can't delete other apps' memberships.

            When deleting a human membership, requires the
            ``chat.memberships`` scope and
            ``spaces/{space}/members/{member}`` format. You can use the
            email as an alias for ``{member}``. For example,
            ``spaces/{space}/members/example@gmail.com`` where
            ``example@gmail.com`` is the email of the Google Chat user.

            When deleting an app membership, requires the
            ``chat.memberships.app`` scope and
            ``spaces/{space}/members/app`` format.

            Format: ``spaces/{space}/members/{member}`` or
            ``spaces/{space}/members/app``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
