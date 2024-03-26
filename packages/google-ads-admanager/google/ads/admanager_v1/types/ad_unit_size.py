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

from google.ads.admanager_v1.types import environment_type_enum
from google.ads.admanager_v1.types import size as gaa_size

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "AdUnitSize",
    },
)


class AdUnitSize(proto.Message):
    r"""Represents the size, environment, and companions of an ad in
    an ad unit.

    Attributes:
        size (google.ads.admanager_v1.types.Size):
            Required. The Size of the AdUnit.
        environment_type (google.ads.admanager_v1.types.EnvironmentTypeEnum.EnvironmentType):
            Required. The EnvironmentType of the AdUnit
        companions (MutableSequence[google.ads.admanager_v1.types.Size]):
            The companions for this ad unit size. Companions are only
            valid if the environment is
            [VIDEO_PLAYER][google.ads.admanager.v1.EnvironmentTypeEnum.EnvironmentType].
    """

    size: gaa_size.Size = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gaa_size.Size,
    )
    environment_type: environment_type_enum.EnvironmentTypeEnum.EnvironmentType = (
        proto.Field(
            proto.ENUM,
            number=2,
            enum=environment_type_enum.EnvironmentTypeEnum.EnvironmentType,
        )
    )
    companions: MutableSequence[gaa_size.Size] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=gaa_size.Size,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
