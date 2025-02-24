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
    package="google.maps.weather.v1",
    manifest={
        "CardinalDirection",
        "SpeedUnit",
        "Wind",
        "WindDirection",
        "WindSpeed",
    },
)


class CardinalDirection(proto.Enum):
    r"""Represents a cardinal direction (including ordinal
    directions).

    Values:
        CARDINAL_DIRECTION_UNSPECIFIED (0):
            The cardinal direction is unspecified.
        NORTH (1):
            The north cardinal direction.
        NORTH_NORTHEAST (2):
            The north-northeast secondary intercardinal
            direction.
        NORTHEAST (3):
            The northeast intercardinal direction.
        EAST_NORTHEAST (4):
            The east-northeast secondary intercardinal
            direction.
        EAST (5):
            The east cardinal direction.
        EAST_SOUTHEAST (6):
            The east-southeast secondary intercardinal
            direction.
        SOUTHEAST (7):
            The southeast intercardinal direction.
        SOUTH_SOUTHEAST (8):
            The south-southeast secondary intercardinal
            direction.
        SOUTH (9):
            The south cardinal direction.
        SOUTH_SOUTHWEST (10):
            The south-southwest secondary intercardinal
            direction.
        SOUTHWEST (11):
            The southwest intercardinal direction.
        WEST_SOUTHWEST (12):
            The west-southwest secondary intercardinal
            direction.
        WEST (13):
            The west cardinal direction.
        WEST_NORTHWEST (14):
            The west-northwest secondary intercardinal
            direction.
        NORTHWEST (15):
            The northwest intercardinal direction.
        NORTH_NORTHWEST (16):
            The north-northwest secondary intercardinal
            direction.
    """
    CARDINAL_DIRECTION_UNSPECIFIED = 0
    NORTH = 1
    NORTH_NORTHEAST = 2
    NORTHEAST = 3
    EAST_NORTHEAST = 4
    EAST = 5
    EAST_SOUTHEAST = 6
    SOUTHEAST = 7
    SOUTH_SOUTHEAST = 8
    SOUTH = 9
    SOUTH_SOUTHWEST = 10
    SOUTHWEST = 11
    WEST_SOUTHWEST = 12
    WEST = 13
    WEST_NORTHWEST = 14
    NORTHWEST = 15
    NORTH_NORTHWEST = 16


class SpeedUnit(proto.Enum):
    r"""Represents the unit used to measure speed.

    Values:
        SPEED_UNIT_UNSPECIFIED (0):
            The speed unit is unspecified.
        KILOMETERS_PER_HOUR (1):
            The speed is measured in kilometers per hour.
        MILES_PER_HOUR (2):
            The speed is measured in miles per hour.
    """
    SPEED_UNIT_UNSPECIFIED = 0
    KILOMETERS_PER_HOUR = 1
    MILES_PER_HOUR = 2


class Wind(proto.Message):
    r"""Represents a set of wind properties.

    Attributes:
        direction (google.maps.weather_v1.types.WindDirection):
            The direction of the wind, the angle it is
            coming from.
        speed (google.maps.weather_v1.types.WindSpeed):
            The speed of the wind.
        gust (google.maps.weather_v1.types.WindSpeed):
            The wind gust (sudden increase in the wind
            speed).
    """

    direction: "WindDirection" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="WindDirection",
    )
    speed: "WindSpeed" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="WindSpeed",
    )
    gust: "WindSpeed" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="WindSpeed",
    )


class WindDirection(proto.Message):
    r"""Represents the direction from which the wind originates.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        degrees (int):
            The direction of the wind in degrees (values
            from 0 to 360).

            This field is a member of `oneof`_ ``_degrees``.
        cardinal (google.maps.weather_v1.types.CardinalDirection):
            The code that represents the cardinal
            direction from which the wind is blowing.
    """

    degrees: int = proto.Field(
        proto.INT32,
        number=1,
        optional=True,
    )
    cardinal: "CardinalDirection" = proto.Field(
        proto.ENUM,
        number=2,
        enum="CardinalDirection",
    )


class WindSpeed(proto.Message):
    r"""Represents the speed of the wind.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        value (float):
            The value of the wind speed.

            This field is a member of `oneof`_ ``_value``.
        unit (google.maps.weather_v1.types.SpeedUnit):
            The code that represents the unit used to
            measure the wind speed.
    """

    value: float = proto.Field(
        proto.FLOAT,
        number=1,
        optional=True,
    )
    unit: "SpeedUnit" = proto.Field(
        proto.ENUM,
        number=2,
        enum="SpeedUnit",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
