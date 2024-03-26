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
    package="google.ads.admanager.v1",
    manifest={
        "User",
        "GetUserRequest",
        "ListUsersRequest",
        "ListUsersResponse",
    },
)


class User(proto.Message):
    r"""The User resource.

    Attributes:
        name (str):
            Identifier. The resource name of the User. Format:
            ``networks/{network_code}/users/{user_id}``
        user_id (int):
            Output only. ``User`` ID.
        display_name (str):
            Required. The name of the User. It has a
            maximum length of 128 characters.
        email (str):
            Required. The email or login of the User. In
            order to create a new user, you must already
            have a Google Account.
        role (str):
            Required. The unique Role ID of the User.
            Roles that are created by Google will have
            negative IDs.
        active (bool):
            Output only. Specifies whether or not the
            User is active. An inactive user cannot log in
            to the system or perform any operations.
        external_id (str):
            Optional. An identifier for the User that is
            meaningful to the publisher. This attribute has
            a maximum length of 255 characters.
        service_account (bool):
            Output only. Whether the user is an OAuth2
            service account user. Service account users can
            only be added through the UI.
        orders_ui_local_time_zone (str):
            Optional. The IANA Time Zone Database time zone, e.g.
            "America/New_York", used in the orders and line items UI for
            this User. If not provided, the UI then defaults to using
            the Network's timezone. This setting only affects the UI for
            this user and does not affect the timezone of any dates and
            times returned in API responses.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    user_id: int = proto.Field(
        proto.INT64,
        number=10,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    email: str = proto.Field(
        proto.STRING,
        number=3,
    )
    role: str = proto.Field(
        proto.STRING,
        number=4,
    )
    active: bool = proto.Field(
        proto.BOOL,
        number=6,
    )
    external_id: str = proto.Field(
        proto.STRING,
        number=7,
    )
    service_account: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    orders_ui_local_time_zone: str = proto.Field(
        proto.STRING,
        number=9,
    )


class GetUserRequest(proto.Message):
    r"""Request object for GetUser method.

    Attributes:
        name (str):
            Required. The resource name of the User. Format:
            ``networks/{network_code}/users/{user_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListUsersRequest(proto.Message):
    r"""Request object for ListUsers method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of Users.
            Format: ``networks/{network_code}``
        page_size (int):
            Optional. The maximum number of Users to
            return. The service may return fewer than this
            value. If unspecified, at most 50 users will be
            returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListUsers`` call. Provide this to retrieve the subsequent
            page.

            When paginating, all other parameters provided to
            ``ListUsers`` must match the call that provided the page
            token.
        filter (str):
            Optional. Expression to filter the response.
            See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters
        order_by (str):
            Optional. Expression to specify sorting
            order. See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters#order
        skip (int):
            Optional. Number of individual resources to
            skip while paginating.
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
    skip: int = proto.Field(
        proto.INT32,
        number=6,
    )


class ListUsersResponse(proto.Message):
    r"""Response object for ListUsersRequest containing matching User
    resources.

    Attributes:
        users (MutableSequence[google.ads.admanager_v1.types.User]):
            The User from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of Users. If a filter was included in the
            request, this reflects the total number after the filtering
            is applied.

            ``total_size`` will not be calculated in the response unless
            it has been included in a response field mask. The response
            field mask can be provided to the method by using the URL
            parameter ``$fields`` or ``fields``, or by using the
            HTTP/gRPC header ``X-Goog-FieldMask``.

            For more information, see
            https://developers.google.com/ad-manager/api/beta/field-masks
    """

    @property
    def raw_page(self):
        return self

    users: MutableSequence["User"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="User",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
