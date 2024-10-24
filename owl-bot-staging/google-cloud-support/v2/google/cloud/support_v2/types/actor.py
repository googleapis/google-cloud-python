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
    package='google.cloud.support.v2',
    manifest={
        'Actor',
    },
)


class Actor(proto.Message):
    r"""An object containing information about the effective user and
    authenticated principal responsible for an action.

    Attributes:
        display_name (str):
            The name to display for the actor. If not
            provided, it is inferred from credentials
            supplied during case creation. When an email is
            provided, a display name must also be provided.
            This will be obfuscated if the user is a Google
            Support agent.
        email (str):
            The email address of the actor. If not
            provided, it is inferred from credentials
            supplied during case creation. If the
            authenticated principal does not have an email
            address, one must be provided. When a name is
            provided, an email must also be provided. This
            will be obfuscated if the user is a Google
            Support agent.
        google_support (bool):
            Output only. Whether the actor is a Google
            support actor.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    email: str = proto.Field(
        proto.STRING,
        number=2,
    )
    google_support: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
