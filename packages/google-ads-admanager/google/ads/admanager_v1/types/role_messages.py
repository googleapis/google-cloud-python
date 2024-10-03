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

from google.ads.admanager_v1.types import role_enums

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "Role",
    },
)


class Role(proto.Message):
    r"""The ``Role`` resource.

    Attributes:
        name (str):
            Identifier. The resource name of the ``Role``. Format:
            ``networks/{network_code}/roles/{role_id}``
        role_id (int):
            Output only. ``Role`` ID.
        display_name (str):
            Required. The display name of the ``Role``.
        description (str):
            Optional. The description of the ``Role``.
        built_in (bool):
            Output only. Whether the ``Role`` is a built-in or custom
            user role.
        status (google.ads.admanager_v1.types.RoleStatusEnum.RoleStatus):
            Output only. The status of the ``Role``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    role_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    built_in: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    status: role_enums.RoleStatusEnum.RoleStatus = proto.Field(
        proto.ENUM,
        number=6,
        enum=role_enums.RoleStatusEnum.RoleStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
