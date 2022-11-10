# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.maps.routing.v2",
    manifest={
        "Maneuver",
    },
)


class Maneuver(proto.Enum):
    r"""A set of values that specify the navigation action to take
    for the current step (e.g., turn left, merge, straight, etc.).
    """
    MANEUVER_UNSPECIFIED = 0
    TURN_SLIGHT_LEFT = 1
    TURN_SHARP_LEFT = 2
    UTURN_LEFT = 3
    TURN_LEFT = 4
    TURN_SLIGHT_RIGHT = 5
    TURN_SHARP_RIGHT = 6
    UTURN_RIGHT = 7
    TURN_RIGHT = 8
    STRAIGHT = 9
    RAMP_LEFT = 10
    RAMP_RIGHT = 11
    MERGE = 12
    FORK_LEFT = 13
    FORK_RIGHT = 14
    FERRY = 15
    FERRY_TRAIN = 16
    ROUNDABOUT_LEFT = 17
    ROUNDABOUT_RIGHT = 18


__all__ = tuple(sorted(__protobuf__.manifest))
