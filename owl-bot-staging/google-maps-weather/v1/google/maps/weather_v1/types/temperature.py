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
    package='google.maps.weather.v1',
    manifest={
        'TemperatureUnit',
        'Temperature',
    },
)


class TemperatureUnit(proto.Enum):
    r"""Represents a unit used to measure temperatures.

    Values:
        TEMPERATURE_UNIT_UNSPECIFIED (0):
            The temperature unit is unspecified.
        CELSIUS (1):
            The temperature is measured in Celsius.
        FAHRENHEIT (2):
            The temperature is measured in Fahrenheit.
    """
    TEMPERATURE_UNIT_UNSPECIFIED = 0
    CELSIUS = 1
    FAHRENHEIT = 2


class Temperature(proto.Message):
    r"""Represents a temperature value.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        degrees (float):
            The temperature value (in degrees) in the
            specified unit.

            This field is a member of `oneof`_ ``_degrees``.
        unit (google.maps.weather_v1.types.TemperatureUnit):
            The code for the unit used to measure the
            temperature value.
    """

    degrees: float = proto.Field(
        proto.FLOAT,
        number=1,
        optional=True,
    )
    unit: 'TemperatureUnit' = proto.Field(
        proto.ENUM,
        number=2,
        enum='TemperatureUnit',
    )


__all__ = tuple(sorted(__protobuf__.manifest))
