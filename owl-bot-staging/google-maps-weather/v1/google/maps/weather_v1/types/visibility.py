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
        'Visibility',
    },
)


class Visibility(proto.Message):
    r"""Represents visibility conditions, the distance at which
    objects can be discerned.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        distance (float):
            The visibility distance in the specified
            unit.

            This field is a member of `oneof`_ ``_distance``.
        unit (google.maps.weather_v1.types.Visibility.Unit):
            The code that represents the unit used to
            measure the distance.
    """
    class Unit(proto.Enum):
        r"""Represents the unit used to measure the visibility distance.

        Values:
            UNIT_UNSPECIFIED (0):
                The visibility unit is unspecified.
            KILOMETERS (1):
                The visibility is measured in kilometers.
            MILES (2):
                The visibility is measured in miles.
        """
        UNIT_UNSPECIFIED = 0
        KILOMETERS = 1
        MILES = 2

    distance: float = proto.Field(
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
