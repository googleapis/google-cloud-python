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

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "User",
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


__all__ = tuple(sorted(__protobuf__.manifest))
