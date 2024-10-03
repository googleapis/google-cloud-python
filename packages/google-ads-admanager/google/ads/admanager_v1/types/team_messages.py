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
        "Team",
    },
)


class Team(proto.Message):
    r"""A Team defines a grouping of users and what entities they
    have access to.

    Attributes:
        name (str):
            Identifier. The resource name of the ``Team``. Format:
            ``networks/{network_code}/teams/{team_id}``
        team_id (int):
            Output only. The unique ID of the Team. This
            value is assigned by Google. Teams that are
            created by Google will have negative IDs.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    team_id: int = proto.Field(
        proto.INT64,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
