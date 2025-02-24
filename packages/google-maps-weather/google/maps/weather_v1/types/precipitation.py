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
        "PrecipitationType",
        "Precipitation",
        "PrecipitationProbability",
        "QuantitativePrecipitationForecast",
    },
)


class PrecipitationType(proto.Enum):
    r"""Represents the type of precipitation at a given location.

    Values:
        PRECIPITATION_TYPE_UNSPECIFIED (0):
            Unspecified precipitation type.
        NONE (8):
            No precipitation.
        SNOW (1):
            Snow precipitation.
        RAIN (2):
            Rain precipitation.
        LIGHT_RAIN (3):
            Light rain precipitation.
        HEAVY_RAIN (4):
            Heavy rain precipitation.
        RAIN_AND_SNOW (5):
            Both rain and snow precipitations.
        SLEET (6):
            Sleet precipitation.
        FREEZING_RAIN (7):
            Freezing rain precipitation.
    """
    PRECIPITATION_TYPE_UNSPECIFIED = 0
    NONE = 8
    SNOW = 1
    RAIN = 2
    LIGHT_RAIN = 3
    HEAVY_RAIN = 4
    RAIN_AND_SNOW = 5
    SLEET = 6
    FREEZING_RAIN = 7


class Precipitation(proto.Message):
    r"""Represents a set of precipitation values at a given location.

    Attributes:
        probability (google.maps.weather_v1.types.PrecipitationProbability):
            The probability of precipitation (values from
            0 to 100).
        qpf (google.maps.weather_v1.types.QuantitativePrecipitationForecast):
            The amount of precipitation (rain or snow),
            measured as liquid water equivalent, that has
            accumulated over a period of time. Note: QPF is
            an abbreviation for Quantitative Precipitation
            Forecast (please see the
            QuantitativePrecipitationForecast definition for
            more details).
    """

    probability: "PrecipitationProbability" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="PrecipitationProbability",
    )
    qpf: "QuantitativePrecipitationForecast" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="QuantitativePrecipitationForecast",
    )


class PrecipitationProbability(proto.Message):
    r"""Represents the probability of precipitation at a given
    location.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        percent (int):
            A percentage from 0 to 100 that indicates the
            chances of precipitation.

            This field is a member of `oneof`_ ``_percent``.
        type_ (google.maps.weather_v1.types.PrecipitationType):
            A code that indicates the type of
            precipitation.
    """

    percent: int = proto.Field(
        proto.INT32,
        number=1,
        optional=True,
    )
    type_: "PrecipitationType" = proto.Field(
        proto.ENUM,
        number=2,
        enum="PrecipitationType",
    )


class QuantitativePrecipitationForecast(proto.Message):
    r"""Represents the expected amount of melted precipitation accumulated
    over a specified time period over a specified area (reference:
    https://en.wikipedia.org/wiki/Quantitative_precipitation_forecast) -
    usually abbreviated QPF for short.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        quantity (float):
            The amount of precipitation, measured as
            liquid water equivalent, that has accumulated
            over a period of time.

            This field is a member of `oneof`_ ``_quantity``.
        unit (google.maps.weather_v1.types.QuantitativePrecipitationForecast.Unit):
            The code of the unit used to measure the
            amount of accumulated precipitation.
    """

    class Unit(proto.Enum):
        r"""Represents the unit used to measure the amount of accumulated
        precipitation.

        Values:
            UNIT_UNSPECIFIED (0):
                Unspecified precipitation unit.
            MILLIMETERS (3):
                The amount of precipitation is measured in
                millimeters.
            INCHES (2):
                The amount of precipitation is measured in
                inches.
        """
        UNIT_UNSPECIFIED = 0
        MILLIMETERS = 3
        INCHES = 2

    quantity: float = proto.Field(
        proto.FLOAT,
        number=1,
        optional=True,
    )
    unit: Unit = proto.Field(
        proto.ENUM,
        number=2,
        enum=Unit,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
