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
        'IceThickness',
    },
)


class IceThickness(proto.Message):
    r"""Represents ice thickness conditions.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        thickness (float):
            The ice thickness value.

            This field is a member of `oneof`_ ``_thickness``.
        unit (google.maps.weather_v1.types.IceThickness.Unit):
            The code that represents the unit used to
            measure the ice thickness.
    """
    class Unit(proto.Enum):
        r"""Represents the unit used to measure the ice thickness.

        Values:
            UNIT_UNSPECIFIED (0):
                The unit is not specified.
            MILLIMETERS (1):
                The thickness is measured in millimeters.
            INCHES (2):
                The thickness is measured in inches.
        """
        UNIT_UNSPECIFIED = 0
        MILLIMETERS = 1
        INCHES = 2

    thickness: float = proto.Field(
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
