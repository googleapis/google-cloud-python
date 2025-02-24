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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.maps.weather.v1',
    manifest={
        'MoonPhase',
        'SunEvents',
        'MoonEvents',
    },
)


class MoonPhase(proto.Enum):
    r"""Marks the moon phase (a.k.a. lunar phase).

    Values:
        MOON_PHASE_UNSPECIFIED (0):
            Unspecified moon phase.
        NEW_MOON (1):
            The moon is not illuminated by the sun.
        WAXING_CRESCENT (2):
            The moon is lit by 0%-50% on its right side
            in the northern hemisphere 🌒 and on its left
            side in the southern hemisphere 🌘.
        FIRST_QUARTER (3):
            The moon is lit by 50.1% on its right side in
            the northern hemisphere 🌓 and on its left side
            in the southern hemisphere 🌗.
        WAXING_GIBBOUS (4):
            The moon is lit by 50%-100% on its right side
            in the northern hemisphere 🌔 and on its left
            side in the southern hemisphere 🌖.
        FULL_MOON (5):
            The moon is fully illuminated.
        WANING_GIBBOUS (6):
            The moon is lit by 50%-100% on its left side
            in the northern hemisphere 🌖 and on its right
            side in the southern hemisphere 🌔.
        LAST_QUARTER (7):
            The moon is lit by 50.1% on its left side in
            the northern hemisphere 🌗 and on its right side
            in the southern hemisphere 🌓.
        WANING_CRESCENT (8):
            The moon is lit by 0%-50% on its left side in
            the northern hemisphere 🌘 and on its right side
            in the southern hemisphere 🌒.
    """
    MOON_PHASE_UNSPECIFIED = 0
    NEW_MOON = 1
    WAXING_CRESCENT = 2
    FIRST_QUARTER = 3
    WAXING_GIBBOUS = 4
    FULL_MOON = 5
    WANING_GIBBOUS = 6
    LAST_QUARTER = 7
    WANING_CRESCENT = 8


class SunEvents(proto.Message):
    r"""Represents the events related to the sun (e.g. sunrise,
    sunset).

    Attributes:
        sunrise_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the sun rises.

            NOTE: In some unique cases (e.g. north of the
            artic circle) there may be no sunrise time for a
            day. In these cases, this field will be unset.
        sunset_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the sun sets.

            NOTE: In some unique cases (e.g. north of the
            artic circle) there may be no sunset time for a
            day. In these cases, this field will be unset.
    """

    sunrise_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    sunset_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class MoonEvents(proto.Message):
    r"""Represents the events related to the moon (e.g. moonrise,
    moonset).

    Attributes:
        moonrise_times (MutableSequence[google.protobuf.timestamp_pb2.Timestamp]):
            The time when the upper limb of the moon appears above the
            horizon (see
            https://en.wikipedia.org/wiki/Moonrise_and_moonset).

            NOTE: For most cases, there'll be a single moon rise time
            per day. In other cases, the list might be empty (e.g. when
            the moon rises after next day midnight). However, in unique
            cases (e.g. in polar regions), the list may contain more
            than one value. In these cases, the values are sorted in
            ascending order.
        moonset_times (MutableSequence[google.protobuf.timestamp_pb2.Timestamp]):
            The time when the upper limb of the moon disappears below
            the horizon (see
            https://en.wikipedia.org/wiki/Moonrise_and_moonset).

            NOTE: For most cases, there'll be a single moon set time per
            day. In other cases, the list might be empty (e.g. when the
            moon sets after next day midnight). However, in unique cases
            (e.g. in polar regions), the list may contain more than one
            value. In these cases, the values are sorted in ascending
            order.
        moon_phase (google.maps.weather_v1.types.MoonPhase):
            The moon phase (a.k.a. lunar phase).
    """

    moonrise_times: MutableSequence[timestamp_pb2.Timestamp] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    moonset_times: MutableSequence[timestamp_pb2.Timestamp] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    moon_phase: 'MoonPhase' = proto.Field(
        proto.ENUM,
        number=3,
        enum='MoonPhase',
    )


__all__ = tuple(sorted(__protobuf__.manifest))
