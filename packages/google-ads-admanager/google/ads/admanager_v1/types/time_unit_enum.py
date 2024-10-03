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
        "TimeUnitEnum",
    },
)


class TimeUnitEnum(proto.Message):
    r"""Wrapper message for TimeUnit."""

    class TimeUnit(proto.Enum):
        r"""Unit of time for the frequency cap.

        Values:
            TIME_UNIT_UNSPECIFIED (0):
                Default value. This value is unused.
            MINUTE (1):
                Minute
            HOUR (2):
                Hour
            DAY (3):
                Day
            WEEK (4):
                Week
            MONTH (5):
                Month
            LIFETIME (6):
                Lifetime
            POD (7):
                Per pod of ads in a video stream. Only valid for entities in
                a VIDEO_PLAYER environment.
            STREAM (8):
                Per video stream. Only valid for entities in a VIDEO_PLAYER
                environment.
        """
        TIME_UNIT_UNSPECIFIED = 0
        MINUTE = 1
        HOUR = 2
        DAY = 3
        WEEK = 4
        MONTH = 5
        LIFETIME = 6
        POD = 7
        STREAM = 8


__all__ = tuple(sorted(__protobuf__.manifest))
