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
    package="google.identity.accesscontextmanager.v1",
    manifest={
        "GcpUserAccessBinding",
    },
)


class GcpUserAccessBinding(proto.Message):
    r"""Restricts access to Cloud Console and Google Cloud APIs for a
    set of users using Context-Aware Access.

    Attributes:
        name (str):
            Immutable. Assigned by the server during creation. The last
            segment has an arbitrary length and has only URI unreserved
            characters (as defined by `RFC 3986 Section
            2.3 <https://tools.ietf.org/html/rfc3986#section-2.3>`__).
            Should not be specified by the client during creation.
            Example:
            "organizations/256/gcpUserAccessBindings/b3-BhcX_Ud5N".
        group_key (str):
            Required. Immutable. Google Group id whose members are
            subject to this binding's restrictions. See "id" in the [G
            Suite Directory API's Groups resource]
            (https://developers.google.com/admin-sdk/directory/v1/reference/groups#resource).
            If a group's email address/alias is changed, this resource
            will continue to point at the changed group. This field does
            not accept group email addresses or aliases. Example:
            "01d520gv4vjcrht".
        access_levels (MutableSequence[str]):
            Required. Access level that a user must have to be granted
            access. Only one access level is supported, not multiple.
            This repeated field must have exactly one element. Example:
            "accessPolicies/9522/accessLevels/device_trusted".
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    group_key: str = proto.Field(
        proto.STRING,
        number=2,
    )
    access_levels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
